import streamlit as st
import asyncio
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import time
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ChatBot')))

import Agent

def chat():
    global user_info_1, user_info_2, user_info_3, user_info_4

    user_info_1 = None
    user_info_2 = None
    user_info_3 = None
    user_info_4 = None
    if 'user_profile' in st.session_state:
        user_info_1 = st.session_state.user_profile[0]
        user_info_2 = st.session_state.user_profile[1]
        user_info_3 = st.session_state.user_profile[2]
        user_info_4 = st.session_state.user_profile[3]

    print("user_info:", user_info_4)

    st.markdown("<h1 style='text-align: center; color: white; margin-top: -20px'>Amazon PayBot</h1>", unsafe_allow_html=True)

    
    button_dic = {"aws_billing": "AWS Billing", 
                  "amz_pay": "Amazon Pay Services", 
                  "amz_prime": "Amazon Prime services",
                  "amz_ecommerce": "Amazon Ecommerce Services"
                  }
    
    with st.chat_message("assistant"):
        st.markdown(f"Hello {user_info_4}, I'm Amazon PayBot. I can assist you with billing and payment queries related to any Amazon service listed below.")
                # Apply custom CSS for buttons
        st.markdown("""
            <style>
            .stButton>button {
                background-color: white;
                color: black;
                border-radius: 20px;
                font-weight: 200;
                font-size: 12px;
                text-align: center;
                cursor: pointer;
            }
            .stButton>button :hover{
                border-radius: 20px;
                padding: 2px;
                color: black;    
            }
            </style>
        """, unsafe_allow_html=True)

        aws_billing = st.button("AWS Billing")
        amz_pay = st.button("Amazon Pay Services")
        amz_prime = st.button("Amazon Prime services")
        amz_ecommerce = st.button("Amazon Ecommerce Services")


    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    def output(prompt):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Show a progress bar with text updates
        progress_bar = st.progress(0)
        progress_text = st.empty()
        progress_text.text("Connecting...")

        start_time = time.time()

        async def run_agent():
            # Asynchronously fetch response from the agent
            response = await Agent.async_agent_call(user_info_1, user_info_2, user_info_3, prompt)
            return response
        
        response = asyncio.run(run_agent())

        elapsed_time = time.time() - start_time

        for i in range(101):
            if i < 25:
                progress_text.text("Processing your request...")
            elif i < 50:
                progress_text.text("Fetching relevant information...")
            elif i < 75:
                progress_text.text("Formulating a response...")
            else:
                progress_text.text("Finalizing response...")

            progress_bar.progress(i)
            time.sleep(elapsed_time / 100)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


    if aws_billing:
        prompts = f"Have queries regarding {button_dic['aws_billing']}"
        st.chat_message("user").markdown(prompts)
        output(prompts)

    if amz_pay:
        prompts = f"Have queries regarding {button_dic['amz_pay']}"
        st.chat_message("user").markdown(prompts)
        output(prompts)

    if amz_prime:
        prompts = f"Have queries regarding {button_dic['amz_prime']}"
        st.chat_message("user").markdown(prompts)
        output(prompts)

    if amz_ecommerce:
        prompts = f"Have queries regarding {button_dic['amz_ecommerce']}"
        st.chat_message("user").markdown(prompts)
        output(prompts)
 
    # React to user input
    if prompt := st.chat_input("How can I help You"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        output(prompt)
        
# chat()