import streamlit as st
import os
import pandas as pd
import torch
import torch.nn as nn

# Paths and configuration setup
image = os.path.join(os.path.dirname(__file__), '..', 'Images')
path = os.path.join(os.path.dirname(__file__), '..', 'Payment Recommendation', 'recommendation-model', 'cnn_recommendation_model.pth')
data_path = os.path.join(os.path.dirname(__file__), '..', 'Payment Recommendation', 'data', 'success_rate_new.csv')

# Streamlit configuration
st.set_page_config(
    page_title="Amazon",
    page_icon=os.path.join(image, 'logo.png'),
    initial_sidebar_state="expanded",
    layout="wide",
)

# Define the CNN model class
class PaymentMethodCNN(nn.Module):
    def __init__(self):
        super(PaymentMethodCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=(3, 3), padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1)
        self.fc1 = nn.Linear(64 * 8, 128)
        self.fc2 = nn.Linear(128, 8)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.dropout = nn.Dropout(0.25)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension
        x = self.conv1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.sigmoid(self.fc2(x))
        return x

# Load the model
model = torch.load(path, map_location=torch.device('cpu'))

# Function to predict the best payment method
def predict_best_payment_method(model, payment_methods, payment_methods_data):
    assert len(payment_methods_data) == len(payment_methods), "Data for each payment method must be provided."

    # Prepare input tensor
    input_data = []
    for method_data in payment_methods_data:
        input_data.append([method_data['cost'], method_data['cashback'], method_data['success_rate'], method_data['user_history']])
    input_tensor = torch.tensor([input_data], dtype=torch.float32)

    # Model prediction
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)

    return output

# Function to recommend payment method based on item and user data
def order(item, user):
    pay_methods = []
    pay_comp = []
    pay_method_dict = {}

    df = pd.read_csv(data_path)
    success_rate = df["Success_Rate"].tolist()

    for pay in range(len(item["payment_methods"])):
        item_mt = item["payment_methods"][pay]
        user_mt = user["payment_usage"][pay]
        pay_methods.append(item_mt['method'])
        pay_dict = {'cost': item_mt["additional_cost_percentage"], 'cashback': item_mt["cashback_percentage"], 'success_rate': success_rate[pay], 'user_history': user_mt["Usage Count"]}
        pay_method_dict[item_mt['method']] = pay_dict
        pay_comp.append(pay_dict)
    
    best_payment_method = predict_best_payment_method(model, pay_methods, pay_comp)

    return best_payment_method.tolist()[0], pay_methods, pay_method_dict

# Function to format price
def format_price(price):
    return price.replace(",", "")

# Function to recommend payment method and display results
def recommend(item, user):
    recommended_order, pay_method, pay_method_dict = order(item, user)

    # Pair payment methods with their recommendation scores
    payment_recommendation_pairs = list(zip(pay_method, recommended_order))
    
    # Sort the pairs by recommendation scores in descending order
    sorted_payment_methods = [method for method, score in sorted(payment_recommendation_pairs, key=lambda x: x[1], reverse=True)]

    # Prepare icons for each payment method
    # icon_dic = {
    #     'Amazon Pay UPI': 'apay',
    #     'Google Pay': 'gpay',
    #     'PhonePe': 'ppay',
    #     'Credit Card': 'cpay',
    #     'Cash on Delivery': 'codpay',
    #     'Debit Card': 'cpay',
    #     'Net Banking': 'npay',
    #     'EMI': 'epay'
    # }

    # Display item details and billing information
    price_without_commas = float(format_price(item['price'].split()[1]))
    total_price = price_without_commas + float(40)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
            <div style='display: flex; align-items: center;'>
                <div style='flex: 0 0 150px;'>
                    <img src='{}' style='height: 150px; width: 150px; object-fit: cover;'>
                </div>
                <div style='flex: 1; padding-left: 20px;'>
                    <div style='font-size: 30px; font-weight: 400;'>{}</div>
                </div>
            </div>
            <hr style='margin: 20px 0;'>
        """.format(item['image'], item['name']), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='border: 1px solid #ccc; padding: 20px; border-radius: 10px;'>
                <h3 style='text-align: center;'>Billing Details</h3>
                <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                    <span style='text-align: left;'>Item:</span>
                    <span style='text-align: right;'>Rs {}</span>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                    <span style='text-align: left;'>Delivery:</span>
                    <span style='text-align: right;'>Rs 40</span>
                </div>
                <hr style='margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                    <span style='text-align: left;'>Order:</span>
                    <span style='text-align: right;'>Rs {}</span>
                </div>
            </div>
        """.format(price_without_commas, total_price), unsafe_allow_html=True)

    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

    # Display payment options as radio buttons with icons
    with st.container(border=4):
        st.markdown("<h3 style='text-align: center;'>Payment Options</h3>", unsafe_allow_html=True)

        data, select = st.columns(2)
            # Create a DataFrame for payment method details
        with data:
            payment_details = {
            'Payment Method': [],
            'Cashback (%)': [],
            'Additional Cost (%)': [],
            'Total Cost (Rs)': []
            }

            for method in sorted_payment_methods:
                cashback_amount = (pay_method_dict[method]['cashback'] / 100) * total_price
                additional_cost_amount = (pay_method_dict[method]['cost'] / 100) * total_price
                final_total = total_price - cashback_amount + additional_cost_amount
                
                payment_details['Payment Method'].append(method)
                payment_details['Cashback (%)'].append(pay_method_dict[method]['cashback'])
                payment_details['Additional Cost (%)'].append(pay_method_dict[method]['cost'])
                payment_details['Total Cost (Rs)'].append(round(final_total, 2))

            df_payment_details = pd.DataFrame(payment_details)

            # Display the DataFrame
            st.dataframe(df_payment_details)

        with select:
            option = st.selectbox(
                "Payment Options",
                sorted_payment_methods,
                index=None,
                placeholder="Select payment method...",
            )

            # Store selected payment method in session state
            if option in pay_method_dict:
                if 'pay' not in st.session_state:
                    st.session_state.pay = pay_method_dict[option]
                    st.session_state.method = option
                st.switch_page("pages/pay.py")
            

# Check if item and user are in session state, otherwise switch to login page
if 'item' and 'user' in st.session_state:
    recommend(st.session_state.item, st.session_state.user)
else:
    st.switch_page("pages/login.py")
