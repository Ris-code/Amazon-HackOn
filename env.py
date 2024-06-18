import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]
os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
os.environ["HF_TOKEN"] = st.secrets["HF_TOKEN"]
os.environ["MONGO_CONNECTION_STRING"] = st.secrets["MONGO_CONNECTION_STRING"]
# os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
# os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")