import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import torch
import torch.nn as nn

image = os.path.join(os.path.dirname(__file__), '..', 'Images')
path = os.path.join(os.path.dirname(__file__), '..', 'Payment Recommendation', 'recommendation-model', 'cnn_recommendation_model.pth')
data_path = os.path.join(os.path.dirname(__file__), '..', 'Payment Recommendation', 'data', 'success_rate_new.csv')

st.set_page_config(
    page_title="Amazon",
    page_icon=os.path.join(image, 'logo.png'),
    initial_sidebar_state="expanded",
    layout="wide",
)

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

def order(item, user):
    pay_methods = []
    pay_comp = []
    df = pd.read_csv(data_path)
    success_rate = df["Success_Rate"].tolist()

    for pay in range(len(item["payment_methods"])):
        item_mt = item["payment_methods"][pay]
        user_mt = user["payment_usage"][pay]
        pay_methods.append(item_mt['method'])
        # print(item_mt)
        pay_dict = {'cost': item_mt["additional_cost_percentage"], 'cashback': item_mt["cashback_percentage"], 'success_rate': success_rate[pay], 'user_history': user_mt["Usage Count"]}
        pay_comp.append(pay_dict)
    
    # print(pay_comp)
    
    best_payment_method = predict_best_payment_method(model, pay_methods, pay_comp)
    print(best_payment_method)

    return best_payment_method.tolist()[0], pay_methods

def format_price(price):
    return price.replace(",", "")

def recommend(item, user):
    recommended_order, pay_method = order(item, user)
    print("recommended:", recommended_order)
    print("pay method:", pay_method)
     # Pair payment methods with their recommendation scores
    payment_recommendation_pairs = list(zip(pay_method, recommended_order))
    
    # Sort the pairs by recommendation scores in descending order
    sorted_payment_methods = [method for method, score in sorted(payment_recommendation_pairs, key=lambda x: x[1], reverse=True)]

    # Print the sorted list
    print(sorted_payment_methods)

    price_without_commas = format_price(item['price'].split()[1])
    total_price = float(price_without_commas) + float(40)

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

    icon_dic = {'Amazon Pay UPI': 'amazon', 'Google Pay': 'google', 'PhonePe': 'phone', 'Credit Card': 'credit-card-fill', 'Cash on Delivery': 'cash', 'Debit Card': 'credit-card-2-front-fill', 'Net Banking': 'bank', 'EMI': 'cash-coin'}
    icons = []
    for i in sorted_payment_methods:
        icons.append(icon_dic[i])

    with st.container(border=4):
        st.markdown("<h3 style='text-align: center;'>Payment Options</h3>", unsafe_allow_html=True)

        main_choice = option_menu(
            menu_title="",
            options=sorted_payment_methods,
            icons=icons,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": "transparent", "margin-top": "10px"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "color": "white"
                },
                "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
            }
        )

if 'item' and 'user' in st.session_state:
    recommend(st.session_state.item, st.session_state.user)
else:
    st.switch_page("pages/login.py")

# recommend({
#         "name": "iPhone 15 Pro Max",
#         "price": "Rs 1,48,000",
#         "image": "https://m.media-amazon.com/images/I/61Jrsu9d3-L._SX679_.jpg",
#         "payment_methods": [
#             {"method": "Amazon Pay UPI", "cashback_percentage": 20.0, "additional_cost_percentage": 0.8},
#             {"method": "Google Pay", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
#             {"method": "PhonePe", "cashback_percentage": 13.5, "additional_cost_percentage": 0.0},
#             {"method": "Credit Card", "cashback_percentage": 20.0, "additional_cost_percentage": 0.4},
#             {"method": "Debit Card", "cashback_percentage": 10.0, "additional_cost_percentage": 0.3},
#             {"method": "EMI", "cashback_percentage": 25.0, "additional_cost_percentage": 6.8},
#             {"method": "Net Banking", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
#             {"method": "Cash on Delivery", "cashback_percentage": 5.0, "additional_cost_percentage": 2.0}
#         ]
#     },
#     {
#   "Name": "Rishav",
#   "Age": 20,
#   "Gender": "Male",
#   "Location": "Noida, UP",
#   "Account Age": "3 years",
#   "Visit Frequency": "5 visits in the last 10 days",
#   "Purchase Frequency": "4 purchases in the last month",
#   "Average Purchase Value": "Rs 3000 per purchase",
#   "Cart Abandonment Rate": "3 abandoned carts in the last month",
#   "Engagement with Promotions": "Clicked on 3 promotional emails in the last month",
#   "Wishlist Activity": "Added 5 items to wishlist in the last month",
#   "Browsing History": [
#     "Laptops",
#     "Smartphones",
#     "Books"
#   ],
#   "Subscription Status": "No",
#   "Preferred Payment Methods": [
#     "Credit Card",
#     "Amazon Pay",
#     "UPI",
#     "Debit Card"
#   ],
#   "user_id": "rishav@gmail.com",
#   "Previous Orders": [
#     {
#       "Item Name": "Laptop",
#       "Cost": "Rs 50,000",
#       "Payment Method": "Credit Card",
#       "Additional Cost": "Rs 2",
#       "Cashback": "Rs 400",
#       "Transaction ID": "afc24751-917c-4b01-a55f-f1876441968a"
#     },
#     {
#       "Item Name": "Smartphone",
#       "Cost": "Rs 20,000",
#       "Payment Method": "Amazon Pay",
#       "Additional Cost": "Rs 0",
#       "Cashback": "Rs 1000",
#       "Transaction ID": "79dbadef-7ec6-4fa4-9d03-08f8eed9469d"
#     },
#     {
#       "Item Name": "Headphones",
#       "Cost": "Rs 5000",
#       "Payment Method": "Debit Card",
#       "Additional Cost": "Rs 100",
#       "Cashback": "Rs 200",
#       "Transaction ID": "8aa2c964-4dd6-4e06-9fa0-fc5218cade1c"
#     },
#     {
#       "Item Name": "Fitness Tracker",
#       "Cost": "Rs 3000",
#       "Payment Method": "UPI",
#       "Additional Cost": "Rs 0",
#       "Cashback": "Rs 150",
#       "Transaction ID": "e229b57f-d327-4ce0-9ee7-c6dbd4679553"
#     }
#   ],
#   "payment_usage": [
#     {
#       "Payment Method": "Amazon Pay UPI",
#       "Usage Count": 12
#     },
#     {
#       "Payment Method": "Google Pay",
#       "Usage Count": 25
#     },
#     {
#       "Payment Method": "PhonePe",
#       "Usage Count": 13
#     },
#     {
#       "Payment Method": "Credit Card",
#       "Usage Count": 14
#     },
#     {
#       "Payment Method": "Debit Card",
#       "Usage Count": 10
#     },
#     {
#       "Payment Method": "EMI",
#       "Usage Count": 0
#     },
#     {
#       "Payment Method": "Net Banking",
#       "Usage Count": 2
#     },
#     {
#       "Payment Method": "Cash on Delivery",
#       "Usage Count": 3
#     }
#   ]
# })