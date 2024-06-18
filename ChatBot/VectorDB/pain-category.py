import os
import time
from langchain_mistralai import ChatMistralAI
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

def document_split(data):
    # Initialize an empty list to store Document objects
    documents = []
    
    # Iterate over the dictionary items
    for query, category in data.items():
        # Construct content and metadata for each query
        content = f"Query: {query}\nCategory: {category}"
        
        metadata = {
            "query": query,
            "category": category
        }

        documents.append(Document(page_content=content, metadata=metadata))

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Split documents into chunks
    all_splits = text_splitter.split_documents(documents)

    return all_splits

def pinecone_vector_store(data):
    index_name = "pain-category"  
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
        print("The index already exists so enter a new index name")

    index = pc.Index(index_name)

    docs = document_split(data)

    PineconeVectorStore.from_documents(docs, embedding=MistralAIEmbeddings(), index_name=index_name)

query_category = {
    "Payment Failure": "High Pain, High Importance",
    "Order Confirmation": "High Pain, High Importance",
    "Delayed Refunds": "High Pain, High Importance",
    "Security Concern": "High Pain, High Importance",
    "International Payments": "High Pain, Low Importance",
    "Hidden Fees": "High Pain, Low Importance",
    "Transaction Limit": "Low Pain, Low Importance",
    "Loyalty Points and Gift cards": "Low Pain, Low Importance",
    "Promo codes and discount issues": "Low Pain, Low Importance",
    "Complex checkout process": "Low Pain, High Importance",
    "Payment options": "Low Pain, High Importance",
    "EMI & Installments": "Low Pain, High Importance",
    "Confusing Payment options": "Low Pain, High Importance"
}

pinecone_vector_store(query_category)
