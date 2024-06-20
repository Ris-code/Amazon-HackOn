import streamlit as st
import os

image = os.path.join(os.path.dirname(__file__), '..', 'Images')
path = os.path.join(os.path.dirname(__file__), '..', 'Payment Recommendation', 'recommendation-model', 'cnn_recommendation_model.pth')
data_path = os.path.join(os.path.dirname(__file__), '..', 'Payment Recommendation', 'data', 'success_rate_new.csv')

st.set_page_config(
    page_title="Amazon",
    page_icon=os.path.join(image, 'logo.png'),
    initial_sidebar_state="expanded",
    layout="wide",
)

def format_price(price):
    return price.replace(",", "")

def pay(item, selected_method, method):
    price = float(format_price(item['price'].split()[1]))
    additional_cost = selected_method['cost'] * price * 0.01
    cashback = selected_method['cashback'] * price * 0.01
    delivery = 40
    total = price + additional_cost - cashback + delivery
    total = round(total, 2)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
            <div style='display: flex; align-items: center;'>
                <div style='flex: 0 0 150px;'>
                    <img src='{item['image']}' style='height: 150px; width: 150px; object-fit: cover;'>
                </div>
                <div style='flex: 1; padding-left: 20px;'>
                    <div style='font-size: 30px; font-weight: 400;'>{item['name']}</div>
                </div>
            </div>
            <hr style='margin: 20px 0;'>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style='border: 1px solid orange;'>
            <div style='font-size: 20px; font-weight: 400; text-align: center; margin-top: 10px;'>Selected Payment Method</div>
            <div style='font-size: 24px; font-weight: 600; text-align: center; margin-bottom: 10px;'>{method}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='border: 1px solid #ccc; padding: 20px; border-radius: 10px;'>
            <h3 style='text-align: center;'>Billing Details</h3>
            <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                <span style='text-align: left;'>Item:</span>
                <span style='text-align: right;'>Rs {}</span>
            </div>
            <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                <span style='text-align: left;'>Delivery:</span>
                <span style='text-align: right;'>Rs {}</span>
            </div>
            <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                <span style='text-align: left;'>Cashback:</span>
                <span style='text-align: right;'>Rs -{}</span>
            </div>
            <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                <span style='text-align: left;'>Additional Cost:</span>
                <span style='text-align: right;'>Rs {}</span>
            </div>
            <hr style='margin: 10px 0;'>
            <div style='display: flex; justify-content: space-between; font-size: 20px;'>
                <span style='text-align: left;'>Total:</span>
                <span style='text-align: right;'>Rs {}</span>
            </div>
        </div>
    """.format(price, delivery, cashback, additional_cost, total), unsafe_allow_html=True)

    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

    _, _ , _ , col1, col2 , _ ,_,_ = st.columns(8)

    with col1:
        if st.button('Cancel', use_container_width=True):
            st.session_state.pop('item', None)
            st.session_state.pop('pay', None)
            st.session_state.pop('method', None)
            st.switch_page("pages/login.py")

    with col2:
        if st.button('Pay Now', use_container_width=True):
            st.switch_page("pages/success.py")

if 'item' in st.session_state and 'pay' in st.session_state and 'method' in st.session_state:
    pay(st.session_state.item, st.session_state.pay, st.session_state.method)
else:
    st.switch_page("pages/login.py")
# pay({
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
#     }, {'cost': 0.1, 'cashback': 6.0, 'success_rate': 0.95, 'user_history': 14}, 'Amazon Pay UPI')