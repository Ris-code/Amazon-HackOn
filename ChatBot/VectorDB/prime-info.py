import os
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema import Document
import re
from dotenv import load_dotenv


load_dotenv()

os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY_ASHU")

def document_split(documents, chunk_size=500, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits

def split(documents, chunk_size=1000, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits

def pinecone_vector_store(docs):
    index_name = "prime-info"
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    else:
        print(f"The index '{index_name}' already exists.")

    index = pc.Index(index_name)
    
    PineconeVectorStore.from_documents(docs, embedding=MistralAIEmbeddings(), index_name=index_name)


def clean_text(text):
    # Remove excessive newlines and whitespace
    text = re.sub(r'\n\s*\n', '\n', text.strip())
    
    # Remove large sections of repetitive and irrelevant content
    sections_to_remove = [
        
    ]


    for section in sections_to_remove:
        text = re.sub(section, '', text, flags=re.MULTILINE)

    # Further clean up to remove any extra lines left
    text = re.sub(r'\n\s*\n', '\n', text.strip())

    # Remove any leading or trailing whitespace from lines
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())

    return text

links = [
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G6LDPN7YJHYKH2J6" , # Amazon Prime 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GR2WKYLHWHLVK6R9" , # Prime Eligible Items 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G202052400" , # Using Promotional Codes 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G2B9L3YR7LR8J4XP" , # Amazon Prime Terms and Conditions 
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=ThyddI41U7z097zqaL" , # Amazon Prime Shopping Edition FAQs
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GRPQFCNVUDYCBG24" , # Amazon Prime Shipping Benefits
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G6LDPN7YJHYKH2J6" , # Amazon Prime and Amazon Prime Lite Memberships 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GFB8K8XHDLQLPB7W" , # Buy More Save More 
    "https://www.amazon.in/b?ie=UTF8&node=10882806031" , # Prime Video
    "https://www.amazon.in/music/prime" , # Prime Music 
    "https://www.amazon.in/l/11486823031" , # Prime Deals and Offers 
    "https://www.amazon.in/cbcc/marketpage" , # Credit Cards Rewards 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G6RZ3AA6NQMCKYEM" , # Sign UP for amazon prime 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G9CYMSKLSARCH96M" , # Manage Member Ship 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GTJQ7QZY7QL2HK4Y" , # End Memebership 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G34EUPKVMYFW8N2U" , # Amazon Prime Membership Fee 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G2B9L3YR7LR8J4XP" , # Amazon Prime Terms and Coditions 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G202201710" , # Recurring Payments for Amazon Prime Terms 

]

for link in links:
    loader = WebBaseLoader(link)
    data = loader.load()
    # Extract text from the loaded document(s) and clean it
    cleaned_documents = []
    for doc in data:
        cleaned_content = clean_text(doc.page_content)
        cleaned_doc = Document(page_content=cleaned_content, metadata=doc.metadata)
        cleaned_documents.append(cleaned_doc)

    # Now cleaned_documents contain the cleaned content in document form
    print("link:",link)
    # Split cleaned documents into smaller chunks
    split_documents = split(cleaned_documents)

    for i in split_documents:
    # Process and store each chunk in Pinecone
        pinecone_vector_store([i])