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

    if 'user_profile' in st.session_state:
        user_info_1 = st.session_state.user_profile[0]
        user_info_2 = st.session_state.user_profile[1]
        user_info_3 = st.session_state.user_profile[2]
        user_info_4 = st.session_state.user_profile[3]
    # user_info_1 = user_profile[0]
    # user_info_2 = user_profile[1]
    # user_info_3 = user_profile[2]
    # user_info_4 = user_profile[3]

    print("user_info:",user_info_4)

    st.markdown("<h1 style='text-align: center; color: white; margin-top: -20px'>Amazon PayBot</h1>", unsafe_allow_html=True)
    # print

    with st.chat_message("assistant"):
        st.markdown(f"Hello {user_info_4}, I'm Amazon PayBot. Please feel free to ask any questions you have regarding payments.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("How can I help you ?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)

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

