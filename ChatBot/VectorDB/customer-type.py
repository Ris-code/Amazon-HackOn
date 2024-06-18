import sys
import os
from langchain_mistralai import ChatMistralAI
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

def document_split(data):
    # Initialize an empty list to store Document objects
    documents = []

    # Convert dictionaries to Document objectsa
    for user in data:
        # Construct content and metadata for each user type
        characteristics = ', '.join([f"{ch['attribute']}: {ch['value']}" for ch in user['characteristics']])
        needs = ', '.join(user['needs'])
        content = f"User Type: {user['user_type']}\nCharacteristics: {characteristics}\nNeeds: {needs}"

        metadata = {
            "user_type": user["user_type"],
            "age": next(ch["value"] for ch in user["characteristics"] if ch["attribute"] == "Age"),
            "location": next(ch["value"] for ch in user["characteristics"] if ch["attribute"] == "Location"),
            "visit_frequency": next(ch["value"] for ch in user["characteristics"] if ch["attribute"] == "Visit Frequency")
        }

        documents.append(Document(page_content=content, metadata=metadata))

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Split documents into chunks
    all_splits = text_splitter.split_documents(documents)

    return all_splits

def pinecone_vector_store(customer_types):
    index_name = "customer"  
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
        print("The index already exist so enter a new index name")

    index = pc.Index(index_name)

    docs = document_split(customer_types)

    PineconeVectorStore.from_documents(docs, embedding=MistralAIEmbeddings(), index_name=index_name)

     
customer_types = [
    {
        "user_type": "Frequent Shoppers",
        "characteristics": [
            {"attribute": "Age", "value": "25-45"},
            {"attribute": "Location", "value": "Varies"},
            {"attribute": "Visit Frequency", "value": "10+ times in the last 10 days"},
            {"attribute": "Purchase Frequency", "value": "High"},
            {"attribute": "Average Purchase Value", "value": "Moderate to High"},
            {"attribute": "Subscription Status", "value": "No"},
            {"attribute": "Device Usage", "value": "Multiple Devices"}
        ],
        "needs": [
            "Easy-to-use payment options",
            "Loyalty rewards and cashback offers",
            "Budget tracking and management tools"
        ]
    },
    {
        "user_type": "Prime Members",
        "characteristics": [
            {"attribute": "Age", "value": "25-45"},
            {"attribute": "Location", "value": "Varies"},
            {"attribute": "Visit Frequency", "value": "5-10 times in the last 10 days"},
            {"attribute": "Subscription Status", "value": "Prime Member"},
            {"attribute": "Spending Behavior", "value": "Moderate to High"},
            {"attribute": "Preferred Payment Methods", "value": "Credit Card"},
            {"attribute": "Engagement with Promotions", "value": "High"}
        ],
        "needs": [
            "Exclusive payment methods or incentives",
            "Enhanced financial tools as part of their Subscription"
        ]
    },
    {
        "user_type": "Millennials and Gen Z",
        "characteristics": [
            {"attribute": "Age", "value": "18-35"},
            {"attribute": "Location", "value": "Urban"},
            {"attribute": "Visit Frequency", "value": "Varies"},
            {"attribute": "Subscription Status", "value": "No"},
            {"attribute": "Tech Savviness", "value": "High"},
            {"attribute": "Device Usage", "value": "Mobile"},
            {"attribute": "Engagement with Promotions", "value": "High"},
            {"attribute": "Preferred Payment Methods", "value": "Mobile Wallet"}
        ],
        "needs": [
            "Innovative payment solutions (e.g., mobile wallets, buy now, pay later options)",
            "Financial education and budgeting tools"
        ]
    },
    {
        "user_type": "Small Business Owners (Sellers on Amazon)",
        "characteristics": [
            {"attribute": "Age", "value": "30-60"},
            {"attribute": "Location", "value": "Varies"},
            {"attribute": "Visit Frequency", "value": "Varies"},
            {"attribute": "Subscription Status", "value": "No"},
            {"attribute": "Sales Channel", "value": "Primary or Secondary on Amazon"},
            {"attribute": "Transaction Volume", "value": "High"},
            {"attribute": "Preferred Payment Methods", "value": "Varies"},
            {"attribute": "Engagement with Promotions", "value": "Varies"}
        ],
        "needs": [
            "Comprehensive financial dashboards",
            "Integrated payment solutions",
            "Tools for managing revenue, expenses, and taxes"
        ]
    },
    {
        "user_type": "Budget-Conscious Consumers",
        "characteristics": [
            {"attribute": "Age", "value": "18-65"},
            {"attribute": "Location", "value": "Varies"},
            {"attribute": "Subscription Status", "value": "No"},
            {"attribute": "Visit Frequency", "value": "1-3 times in the last 10 days"},
            {"attribute": "Income Level", "value": "Low"},
            {"attribute": "Spending Behavior", "value": "Frugal"},
            {"attribute": "Preferred Payment Methods", "value": "Debit Card or Cash"},
            {"attribute": "Engagement with Promotions", "value": "Low"}
        ],
        "needs": [
            "Budgeting and saving tools",
            "Payment plans and installment options",
            "Financial education resources"
        ]
    },
    {
        "user_type": "Elderly Customers",
        "characteristics": [
            {"attribute": "Age", "value": "greater than 65"},
            {"attribute": "Location", "value": "Varies"},
            {"attribute": "Visit Frequency", "value": "1-3 times in the last 10 days"},
            {"attribute": "Subscription Status", "value": "No"},
            {"attribute": "Tech Savviness", "value": "Low to Moderate"},
            {"attribute": "Income Management", "value": "Fixed Income"},
            {"attribute": "Preferred Payment Methods", "value": "Credit Card or Debit Card or Cash on Delivery"},
            {"attribute": "Engagement with Promotions", "value": "Low"}
        ],
        "needs": [
            "Simplified, secure payment interfaces",
            "Tools to manage fixed incomes and budgeting",
            "Fraud protection and financial advice"
        ]
    }
]

# pinecone_vector_store(customer_types)