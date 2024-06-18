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

os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# Define a function to split documents into chunks

def document_split(documents, chunk_size=500, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits

def split(documents, chunk_size=1000, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits

def pinecone_vector_store(docs):
    index_name = "policy"
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
        r"Skip to main content",
        r"\.in",
        r"Delivering to .*",
        r"Update location",
        r"Upload a JPEG, PNG, WEBP, GIF, SVG, AVIF, BMP or ICO image file.",
        r"Upload an image file size of 5 MB or less.",
        r"Upload an image",
        r"All Categories",
        r"Alexa Skills",
        r"Appliances",
        r"Apps & Games",
        r"Audible Audiobooks",
        r"Baby",
        r"Beauty",
        r"Books",
        r"Car & Motorbike",
        r"Clothing & Accessories",
        r"Collectibles",
        r"Computers & Accessories",
        r"Deals",
        r"Electronics",
        r"Furniture",
        r"Garden & Outdoors",
        r"Gift Cards",
        r"Grocery & Gourmet Foods",
        r"Health & Personal Care",
        r"Home & Kitchen",
        r"Industrial & Scientific",
        r"Jewellery",
        r"Kindle Store",
        r"Luggage & Bags",
        r"Luxury Beauty",
        r"Movies & TV Shows",
        r"MP3 Music",
        r"Music",
        r"Musical Instruments",
        r"Office Products",
        r"Pet Supplies",
        r"Prime Video",
        r"Shoes & Handbags",
        r"Software",
        r"Sports, Fitness & Outdoors",
        r"Subscribe & Save",
        r"Tools & Home Improvement",
        r"Toys & Games",
        r"Under ₹500",
        r"Video Games",
        r"Watches",
        r"Search Amazon\.in",
        r"Returns\n& Orders",
        r"Cart",
        r"Mobiles",
        r"Fashion",
        r"Electronics",
        r"Prime",
        r"New Releases",
        r"Home & Kitchen",
        r"Customer Service",
        r"Computers",
        r"Books",
        r"Car & Motorbike",
        r"Gift Ideas",
        r"Sports, Fitness & Outdoors",
        r"Beauty & Personal Care",
        r"Home Improvement",
        r"Toys & Games",
        r"Grocery & Gourmet Foods",
        r"Gift Cards",
        r"Custom Products",
        r"Baby",
        r"Health, Household & Personal Care",
        r"Video Games",
        r"Pet Supplies",
        r"Audible",
        r"AmazonBasics",
        r"Subscribe & Save",
        r"Coupons",
        r"Kindle eBooks",
        r"Help and Customer Service",
        r"Find more solutions",
        r"Returns , Replacements and Refunds",
        r"›",
        r"About Us",
        r"Careers",
        r"Press Releases",
        r"Connect with Us",
        r"Facebook",
        r"Twitter",
        r"Instagram",
        r"Make Money with Us",
        r"Protect and Build Your Brand",
        r"Become an Affiliate",
        r"Fulfilment by Amazon",
        r"Advertise Your Products",
        r"Let Us Help You",
        r"COVID-19 and Amazon",
        r"Your Account",
        r"Returns Centre",
        r"100% Purchase Protection",
        r"Help",
        r"English",
        r"India",
        r"AbeBooksBooks, art& collectibles",
        r"AudibleDownloadAudio Books",
        r"IMDbMovies, TV& Celebrities",
        r"ShopbopDesignerFashion Brands",
        r"Prime Now 2-Hour Deliveryon Everyday Items",
        r"Conditions of Use & Sale",
        r"Privacy Notice",
        r"Interest-Based Ads",
        r"© 1996-2024, Amazon.com, Inc. or its affiliates",
        r"Back to top",
        r"Get to Know Us",
        r"Amazon Science",
        r"Sell on Amazon",
        r"Sell under Amazon Accelerator",
        r"Amazon Global Selling",
        r"Amazon Pay on Merchants",
        r"Amazon App Download",
        r"Abe, art& collectibles",
        r"Amazon BusinessEverything ForYour Business",
        r"ShopbopDesigner Brands",
        r"DownloadAudio ",
        r"Amazon Web ServicesScalable CloudComputing Services",
        r"Now 2-Hour Deliveryon Everyday Items",
        r"Amazon  100 million songs, ad-freeOver 15 million podcast episodes © 1996-2024, Amazon.com, Inc. or its affiliates"
    ]

    for section in sections_to_remove:
        text = re.sub(section, '', text, flags=re.MULTILINE)

    # Further clean up to remove any extra lines left
    text = re.sub(r'\n\s*\n', '\n', text.strip())

    # Remove any leading or trailing whitespace from lines
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())

    return text

policy = [
"https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202111770", # REFUND
"https://www.amazon.in/gp/help/customer/display.html/ref=cs_ret_rp_q_1?nodeId=202111910", # RETURN
"https://www.amazon.in/gp/help/customer/display.html?nodeId=G202111750", # REPLACEMENT
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ", # PRIVACY_NOTICE
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GLSBYFE9MGKKQXXM", # CONDITION_OF_USE
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GH79TEB7MQ7SBXPG", # SAFE_ONLINE_SHOPPING
"https://www.amazon.in/b?node=27277422031&ref=facelanding", # AMAZON_PAY_SAFETY
"https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GMP8PC8KBY5FCPM2", # CHECK_REFUND_STATUS
"https://www.amazon.in/gp/help/customer/display.html?nodeId=201908990", # SECURITY_AND_PRIVACY
"https://www.amazon.in/gp/help/customer/display.html?nodeId=202111950", # RETURN_PICKUP&SELF-SHIP_GUIDELINE
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GQHC9JYSMPRP39RH", # DAMAGE_DEFECTIVE_WRONG_PRODUCT_FAQ
"https://www.amazon.in/gp/help/customer/display.html?nodeId=202084980", # SHIPPING_SPEED&CHARGES
"https://www.amazon.in/gp/help/customer/display.html?nodeId=202085110", # GUARANTEED_SHIPPING_SPEEDSAND_CHARGES
"https://www.amazon.in/gp/help/customer/display.html?nodeId=202054820", # POD
"https://www.amazon.in/gp/help/customer/display.html?nodeId=202054460", # EMI
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GFBWMNXEPYVJAY9A", # ACCEPTED_PAYMENT_METHODS
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GJLLHTPTG32P95DR", # PAYMENT_ISSUES
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GF8B8BP3Q4HQADU8", # RESOLVE_DECLINED_PAYMENT
"https://www.amazon.in/gp/help/customer/display.html?nodeId=GJ626ASQQ6PD2KZY", # AMAZON_PAY_LATER
"https://www.amazon.in/gp/help/customer/display.html?nodeId=G201895730", # TERM_AND_CONDITIONS
"https://www.amazon.in/gp/help/customer/display.html?nodeId=201894450", # PAYMENT_PRICING_PROMOTION
"https://www.amazon.in/gp/help/customer/display.html?nodeId=202212990", # UPI
"https://www.amazon.in/gp/help/customer/display.html?nodeId=G202123450", # AMAZON_PAY
"https://www.amazon.in/gp/help/customer/display.html?nodeId=G202123470", # AMAZON_PAY_BALANCE
"https://www.amazon.in/gp/help/customer/display.html?nodeId=G202054800" # NET_BANKING
]
# Loop through each policy URL
for link in policy:
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
    # print(split_documents)
    # break
    for i in split_documents:
    # Process and store each chunk in Pinecone
        pinecone_vector_store([i])
