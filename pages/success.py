import streamlit as st

st.set_page_config(
    page_title="Payment Success",
    page_icon="✅",
    layout="centered"
)

def payment_success():
    st.markdown("""
        <style>
            .centered-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
                margin-top: -150px;
            }
            .tick-icon {
                font-size: 80px;
                color: green;
            }
            .success-message {
                font-size: 30px;
                font-weight: bold;
                margin-top: 20px;
            }
            .assistance-message {
                font-size: 20px;
                margin-top: 20px;
            }
            .stButton>button {
                font-size: 18px;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: orange;
                color: black;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                margin-top: -210px;
                margin-left: 280px;
            }
            .stButton>button :hover{
                color: white;
            }
        </style>
        </style>
        <div class='centered-content'>
            <div class='tick-icon'>✅</div>
            <div class='success-message'>Payment Successful</div>
            <div class='assistance-message'>
                For further payment assistance and queries, ask our Amazon Bot
            </div>
    """, unsafe_allow_html=True)

    if st.button("Back to Log In"):
        st.switch_page("pages/login.py")

payment_success()