import streamlit as st
import sys
import os
from streamlit_option_menu import option_menu
import base64
from pymongo import MongoClient
import pages.bot as bot

# # Add directories to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ChatBot')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Payment Recommendation')))
image = os.path.join(os.path.dirname(__file__), '..', 'Images')

# # Import the chatbot module
# import chatbot
import user_profile
import env

client = MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
db = client['amazon']
collection = db['user_profiles']
collection_prod = db['Products']


def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# def on_buy_now_click(item):
#     # st.write(f"You clicked 'Buy Now' for {item['name']}")
#     recom.recommend(item)

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
            height: 100%;
            max-height: 300px;  
            object-fit: cover;
            margin-bottom: 10px;
        }
        .price {
            font-size: 17px;
            font-weight: bold;
            background-color: orange;
            color: black;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            width: 100%;
            height: 100%;
            flex: 1;
            padding: 5px;
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
    
def display_home(user, items_cursor):
    # Convert cursor to list to get the length and iterate over items
    items = list(items_cursor)
    len_items = len(items)
    if 'user_profile' not in st.session_state:
            st.session_state.user_profile = user_scarp(user)
    # if 'item' in st.session_state:
    #     del st.session_state['item']
    # st.session_state.item = None

    st.markdown(f"<h1 style='text-align: left; color: white; margin-top: -20px'>Hey {user['Name']}, Welcome to Amazon !!</h1>", unsafe_allow_html=True)
    
       # Clear the selected item from session state if returning to the home page
    if st.session_state.get("current_page") != "Home":
        st.session_state["current_page"] = "Home"
        if 'item' in st.session_state:
            del st.session_state['item']
    # Calculate the number of rows needed
    rows = [st.columns(3) for _ in range(len_items // 3)]
    if len_items % 3:
        rows.append(st.columns(len_items % 3))

    # Display items in the calculated rows
    item_index = 0
    for row in rows:
        for col in row:
            if item_index < len_items:
                item = items[item_index]
                with col:
                    with st.container(border=2):
                        st.markdown(f'<img src="{item["image"]}" class="custom-image">', unsafe_allow_html=True)
                        st.markdown(f'<div class="item-name">{item["name"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="price">{item["price"]}</div>', unsafe_allow_html=True)
                        if st.button("Buy Now", key=f"buy_now_{item_index}", use_container_width=True):
                            # if 'item' not in st.session_state:
                            st.session_state.item = item
                            st.session_state.current_page = "Recommendation"
                item_index += 1    

@st.cache_data(show_spinner=False)
def user_scarp(_user):
    print(1)
    user_needs, user_attributes, user_type, user_name = user_profile.fetch_user_attributes(_user)
    return [user_needs, user_attributes, user_type, user_name]

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
    
    # if 'user_profile' not in st.session_state:
    #     # user_needs, user_attributes, user_type, user_name = user_profile.fetch_user_attributes(user)
    #     # st.session_state['user_attributes'] = user_attributes
    #     # st.session_state['user_type'] = user_type
    #     # st.session_state['user_needs'] = user_needs
    #     # st.session_state['user_name'] = user_name
    #     st.session_state.user_profile = user_scarp(user)

    if main_choice == "Home":
        items = collection_prod.find()
        
        display_home(user, items)

        # if 'user_profile' not in st.session_state:
        #     st.session_state.user_profile = user_scarp(user)
        
        # user_scarp(user)

    elif main_choice == "Dashboard":
        st.switch_page("pages/finance_manage.py")

    elif main_choice == "About":
        st.write("About")

    elif main_choice == "PayBot":
        # d1 = user_scarp(user)
        bot.chat()

def main():
    st.set_page_config(
        page_title="Amazon",
        page_icon=os.path.join(image, 'logo.png'),
        initial_sidebar_state="expanded",
        layout="wide",
    )

    # if 'user' not in st.session_state:
    #     st.session_state.user = None

    # if st.session_state.user:
    #     # app(st.session_state.user)
    # else:
    # if 'item' in st.session_state:
    #     st.switch_page("pages/recommendation.py")

    if 'user' in st.session_state:
        user = st.session_state.user
        print(user)
        app(user)
    else:
        st.switch_page("pages/login.py")
    
        # Redirect to recommendation page if item is set
    if st.session_state.get("current_page") == "Recommendation" and 'item' in st.session_state:
        st.switch_page("pages/recommendation.py")


if __name__ == "__main__":
    main()
