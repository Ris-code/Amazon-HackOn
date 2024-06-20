import streamlit as st
import sys
import os
from streamlit_option_menu import option_menu
import base64
from pymongo import MongoClient

image = os.path.join(os.path.dirname(__file__), '..', 'Images')

import env

client = MongoClient(env.MONGO_KEY)
db = client['amazon']
collection = db['user_profiles']
collection_prod = db['Products']

def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
def find_user(email):
    user = collection.find_one({"user_id": email})
    return user

def login():
    col1, col2, col3 = st.columns(3)
    with col2:
        with st.container(border=2):
            img_path = os.path.join(image, 'amazon-logo.png')
            img_base64 = img_to_base64(img_path)
            st.markdown(
                f"""<div style='display: flex; align-items: center; justify-content: center; margin-top: -40px; margin-bottom: -50px'>
                <img src='data:image/png;base64,{img_base64}' style='object-cover: True; height: 200px;'/>
                </div>""",
                unsafe_allow_html=True
            )
            st.markdown(f"<h1 style='text-align: center; color: white; margin-top: -20px'>Amazon Login</h1>", unsafe_allow_html=True)
            email = st.text_input("Enter your email:")
            if st.button("Login", key="login_button", use_container_width = True):
                with st.spinner('Verifying user...'):
                    user = find_user(email)

                    if user:
                        if 'user' not in st.session_state:
                            st.session_state.user = None
                        st.session_state.user = user

                        st.success("Login successful!")
                        st.switch_page("pages/home.py")
                    else:
                        st.error("User ID does not exist")
                        

def main():
    st.set_page_config(
        page_title="Amazon",
        page_icon=os.path.join(image, 'logo.png'),
        initial_sidebar_state="expanded",
        layout="wide",
    )
    
    login()

if __name__ == "__main__":
    main()
