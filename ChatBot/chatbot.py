import streamlit as st
from Agent import *
from user_profile import *
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import time

def chat():
    # st.title("Amazon Payment Bot")
    user_needs, user_attributes, user_type, name = fetch_user_attributes("cscsdckls")

    st.markdown("<h1 style='text-align: center; color: white; margin-top: -20px'>Amazon PayBot</h1>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        st.markdown(f"Hello {name}, I'm Amipay. Please feel free to ask any questions you have regarding payments.")

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

        # Fetch the response from the agent in a separate thread or asynchronous call
        response = agent(user_needs, user_attributes, user_type, prompt)

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

# if __name__ == "__main__":
#     chat()
