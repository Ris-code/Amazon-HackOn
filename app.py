# import streamlit as st
# import sys
# import os
# from streamlit_option_menu import option_menu
# import base64
# from pymongo import MongoClient
# # Add directories to sys.path if needed
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ChatBot')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Payment Recommendation')))
# image = os.path.join(os.path.dirname(__file__), 'Images')

# # Import the chatbot module
# import chatbot
# import env

# client = MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))  # Update this with your MongoDB connection string
# db = client['amazon']  # Replace 'amazon' with your database name
# collection = db['user_profiles']  # Replace 'user_profiles' with your collection name

# def img_to_base64(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode()

# def on_buy_now_click(item):
#     st.write(f"You clicked 'Buy Now' for {item['name']}")

# def app(user):
#     # Custom CSS to adjust the image size and position and add transparent effect to nav link
#     custom_css = """
#     <style>
#         .sidebar .sidebar-content {
#             padding-top: 0px;
#         }
#         .custom-sidebar-img {
#             display: block;
#             margin-left: auto;
#             margin-right: auto;
#             width: 50%;  /* Adjust the width as needed */
#             height: auto;  /* Maintain aspect ratio */
#             margin-top: -50px;  /* Adjust the top margin to move the image up */
#         }
#         .nav-link-selected {
#             background-color: rgba(255, 255, 255, 0.3);  /* Transparent white background */
#             color: #141920;  /* Example text color */
#         }
#         .custom-container {
#             background-color: white;  /* Container background color */
#             padding: 10px;
#             border-radius: 10px;
#             min-height: 320px;  /* Minimum height for the container */
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: space-between;
#         }
#         .custom-button {
#             background-color: orange;  /* Button background color */
#             color: black;
#             width: 100%;
#             border: none;
#             padding: 10px;
#             border-radius: 5px;
#             cursor: pointer;
#         }
#         .custom-button:hover {
#             background-color: #e67e22;  /* Button hover color */
#         }
#         .custom-image {
#             width: 100%;  /* Ensure the image is less than the container size */
#             height: auto;
#             max-height: 300px;  /* Adjust the max height as needed */
#             object-fit: cover;
#             margin-bottom: 10px;
#         }
#         .price {
#             font-size: 17px;
#             font-weight: bold;
#             color: black;
#             text-align: center;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             margin-top: 5px;
#             background-color: white;
#             border-radius: 5px;
#             width: 100%;
#             height: 100%;
#             flex: 1;
#         }
#         .item-name {
#             font-size: 16px;
#             font-weight: bold;
#             text-align: center;
#             background-color: #f0f0f0;  /* Light gray background */
#             padding: 5px;
#             color: black;
#             border: 1px solid #ddd;  /* Light border */
#             border-radius: 5px;
#             margin-bottom: 10px;
#         }
#         .custom-buy-now {
#             background-color: orange;
#             color: black;
#             padding: 10px;
#             border-radius: 5px;
#             text-align: center;
#             display: inline-block;
#             cursor: pointer;
#             width: 100%;
#         }
#         .custom-buy-now:hover {
#             background-color: #e67e22;
#         }
#     </style>
#     """
#     st.markdown(custom_css, unsafe_allow_html=True)

#     img_path = os.path.join(image, 'amazon-logo.png')
#     img_base64 = img_to_base64(img_path)

#     # Use HTML to place the image
#     st.sidebar.markdown(
#         f'<img src="data:image/png;base64,{img_base64}" class="custom-sidebar-img" alt="Amazon Logo">',
#         unsafe_allow_html=True
#     )

#     with st.sidebar:
#         main_choice = option_menu(
#             menu_title="",
#             options=["Home", "Dashboard", "About", "PayBot"],
#             icons=["house-fill", "file-bar-graph-fill", "info-circle-fill", "robot"],
#             menu_icon="cast",
#             default_index=0,
#             styles={
#                 "container": {"background-color": "#141920", "margin-top": "-10px"},
#                 "icon": {"color": "orange", "font-size": "25px"}, 
#                 "nav-link": {
#                     "font-size": "16px",
#                     "text-align": "left",
#                     "margin": "0px",
#                     "padding": "10px",
#                     "color": "white"
#                 },
#                 "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
#             }
#         )

#     items = [
#         {"name": "Raymond Yellow Shirt", "price": "Rs 454", "image": "https://m.media-amazon.com/images/I/41B+TiDYZRL.jpg"},
#         {"name": "Noise Pulse Go", "price": "Rs 1,099", "image": "https://m.media-amazon.com/images/I/61akt30bJsL._SX679_.jpg"},
#         {"name": "Iphone 15 Pro Max", "price": "Rs 1,48,000", "image": "https://m.media-amazon.com/images/I/61Jrsu9d3-L._SX679_.jpg"},
#         {"name": "SPARX Mens Sx0706g", "price": "Rs 749", "image": "https://m.media-amazon.com/images/I/41BNwMRUaJL._SY695_.jpg"},
#         {"name": "ZAVERI PEARLS Necklace", "price": "Rs 410", "image": "https://m.media-amazon.com/images/I/71eaAiL-wjL._SY695_.jpg"},
#         {"name": "Body Maxx 78005 Dumbbell", "price": "Rs 1399", "image": "https://m.media-amazon.com/images/I/51cc+xTtHiL._SX679_.jpg"},
#     ]

#     if main_choice == "Home":
#         st.markdown(f"<h1 style='text-align: left; color: white; margin-top: -20px'>Hey {user['Name']}, Welcome to Amazon !!</h1>", unsafe_allow_html=True)

#         rows = [st.columns(3), st.columns(3)]

#         for idx, (col, item) in enumerate(zip(rows[0] + rows[1], items)):
#             with col:
#                 with st.container(border=2):
#                     st.markdown(f'<img src="{item["image"]}" class="custom-image">', unsafe_allow_html=True)
#                     st.markdown(f'<div class="item-name">{item["name"]}</div>', unsafe_allow_html=True)
#                     col1, col2 = st.columns([1, 2])
#                     with col1:
#                         st.markdown(f'<div class="price">{item["price"]}</div>', unsafe_allow_html=True)
#                     with col2:
#                         # button_placeholder = st.empty()
#                         if st.button("Buy Now", key=f"buy_now_{idx}", use_container_width=True):
#                             on_buy_now_click(item)
#                             # button_placeholder.markdown(f'<div class="custom-buy-now">Buy Now</div>', unsafe_allow_html=True)

#     elif main_choice == "Dashboard":
#         st.write("Dashboard")
#     elif main_choice == "About":
#         st.write("About")
#     elif main_choice == "PayBot":
#         with st.spinner("Please hold a moment ...."):
#             chatbot.user(user)
#             chatbot.chat()

# def main():
#     st.set_page_config(
#         page_title="Amazon",
#         page_icon=os.path.join(image, 'amazon.svg'),
#         initial_sidebar_state="expanded",
#         layout="wide",
#     )

#     if 'user' not in st.session_state:
#         st.session_state.user = None

#     if st.session_state.user:
#         app(st.session_state.user)
    
#     else:
#         col1, col2, col3 = st.columns(3)

#         with col2:
#             with st.container(border=2):

#                 # st.title("Amazon Login")
#                 # st.image(os.path.join(image, 'amazon-logo.png'))
#                 img_path = os.path.join(image, 'amazon-logo.png')
#                 img_base64 = img_to_base64(img_path)

#                 st.markdown(
#                     f"<img src='data:image/png;base64,{img_base64}' style='height: 200px; display: flex; align-items: center; justify-content: center; margin-top: -40px;  margin-bottom: -60px; margin-left: 110px;'>",
#                     unsafe_allow_html=True
#                 )
                
#                 st.markdown(f"<h1 style='text-align: center; color: white; margin-top: -20px'>Amazon Login</h1>", unsafe_allow_html=True)
#                 email = st.text_input("Enter your email:")

#                 if st.button("Login", key="login_button"):
#                     # print(user)
#                     with st.spinner('Verifying user...'):
#                         user = collection.find_one({"user_id": email})
#                         if user:
#                             st.session_state.user = user
#                             st.success("Login successful!")
#                             st.rerun()
#                         else:
#                             st.error("User ID does not exist")

# if __name__ == "__main__":
#     main()
import streamlit as st
import sys
import os
from streamlit_option_menu import option_menu
import base64
from pymongo import MongoClient

# Add directories to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ChatBot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Payment Recommendation')))
image = os.path.join(os.path.dirname(__file__), 'Images')

# Import the chatbot module
import chatbot
import env

client = MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
db = client['amazon']
collection = db['user_profiles']
collection_prod = db['Products']

def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def on_buy_now_click(item):
    st.write(f"You clicked 'Buy Now' for {item['name']}")

def set_custom_css():
    custom_css = """
    <style>
        .sidebar .sidebar-content {
            padding-top: 0px;
        }
        .custom-sidebar-img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;  
            height: auto;  
            margin-top: -50px;  
        }
        .nav-link-selected {
            background-color: rgba(255, 255, 255, 0.3);  
            color: #141920;  
        }
        .custom-container {
            background-color: white;  
            padding: 10px;
            border-radius: 10px;
            min-height: 320px;  
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
        }
        .custom-button {
            background-color: orange;  
            color: black;
            width: 100%;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        .custom-button:hover {
            background-color: #e67e22;  
        }
        .custom-image {
            width: 100%;  
            height: auto;
            max-height: 300px;  
            object-fit: cover;
            margin-bottom: 10px;
        }
        .price {
            font-size: 17px;
            font-weight: bold;
            color: black;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 5px;
            background-color: white;
            border-radius: 5px;
            width: 100%;
            height: 100%;
            flex: 1;
        }
        .item-name {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            background-color: #f0f0f0;  
            padding: 5px;
            color: black;
            border: 1px solid #ddd;  
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .custom-buy-now {
            background-color: orange;
            color: black;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            display: inline-block;
            cursor: pointer;
            width: 100%;
        }
        .custom-buy-now:hover {
            background-color: #e67e22;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
def display_home(user, items):
    st.markdown(f"<h1 style='text-align: left; color: white; margin-top: -20px'>Hey {user['Name']}, Welcome to Amazon !!</h1>", unsafe_allow_html=True)
    rows = [st.columns(3), st.columns(3)]

    for idx, (col, item) in enumerate(zip(rows[0] + rows[1], items)):
        with col:
            with st.container(border=2):
                st.markdown(f'<img src="{item["image"]}" class="custom-image">', unsafe_allow_html=True)
                st.markdown(f'<div class="item-name">{item["name"]}</div>', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f'<div class="price">{item["price"]}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Buy Now", key=f"buy_now_{idx}", use_container_width=True):
                        on_buy_now_click(item)

def app(user):
    set_custom_css()
    
    img_path = os.path.join(image, 'amazon-logo.png')
    img_base64 = img_to_base64(img_path)

    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" class="custom-sidebar-img" alt="Amazon Logo">',
        unsafe_allow_html=True
    )

    with st.sidebar:
        main_choice = option_menu(
            menu_title="",
            options=["Home", "Dashboard", "About", "PayBot"],
            icons=["house-fill", "file-bar-graph-fill", "info-circle-fill", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": "#141920", "margin-top": "-10px"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "color": "white"
                },
                "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
            }
        )

    if main_choice == "Home":
        items = collection_prod.find()
        display_home(user, items)

    elif main_choice == "Dashboard":
        st.write("Dashboard")

    elif main_choice == "About":
        st.write("About")
        
    elif main_choice == "PayBot":
        with st.spinner("Please hold a moment ...."):
            chatbot.user(user)
            chatbot.chat()

def login():
    col1, col2, col3 = st.columns(3)
    with col2:
        with st.container(border=2):
            img_path = os.path.join(image, 'amazon-logo.png')
            img_base64 = img_to_base64(img_path)
            st.markdown(
                f"<img src='data:image/png;base64,{img_base64}' style='height: 200px; display: flex; align-items: center; justify-content: center; margin-top: -40px;  margin-bottom: -60px; margin-left: 110px;'>",
                unsafe_allow_html=True
            )
            st.markdown(f"<h1 style='text-align: center; color: white; margin-top: -20px'>Amazon Login</h1>", unsafe_allow_html=True)
            email = st.text_input("Enter your email:")
            if st.button("Login", key="login_button"):
                with st.spinner('Verifying user...'):
                    user = collection.find_one({"user_id": email})
                    if user:
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("User ID does not exist")

def main():
    st.set_page_config(
        page_title="Amazon",
        page_icon=os.path.join(image, 'amazon.svg'),
        initial_sidebar_state="expanded",
        layout="wide",
    )

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        app(st.session_state.user)
    else:
        login()

if __name__ == "__main__":
    main()
