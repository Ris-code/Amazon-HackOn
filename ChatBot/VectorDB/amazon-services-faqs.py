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

os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY_ACCOUNT_2")

def document_split(documents, chunk_size=500, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits

def split(documents, chunk_size=1000, chunk_overlap=0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits

def pinecone_vector_store(docs):
    index_name = "amazon-pay-services-faqs"
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
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G5BMM3G56ZNCWHQT" , # Amazon Pay Flights: MakeMyTrip
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GTSDUMBB6NLXZQYR" , # 
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GR6EU9FRAQ8FDYE4" , # Using Promotional Codes 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GKGXX92SJ88Q9YY2" , # Amazon Prime Terms and Conditions 
    "https://www.amazon.in/gp/help/customer/display.html?ie=UTF8&nodeId=G4WG8S7FTYGWXKJP" , # Amazon Prime Shopping Edition FAQs
    "https://www.amazon.in/gp/help/customer/display.html/ref=cs_apay_t_ip?ie=UTF8&nodeId=G5X8WM52MQ2AM9TG" , # Amazon Prime Shipping Benefits
    "https://www.amazon.in/gp/help/customer/display.html/ref=cs_apay_t_cc?ie=UTF8&nodeId=GKLD2EQBY7FA7KFH" , # Amazon Prime and Amazon Prime Lite Memberships 
    "https://www.amazon.in/gp/help/customer/display.html/ref=cs_apay_t_fast?ie=UTF8&nodeId=GE4GZDWU34D5ZAN4" , # Buy More Save More 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GL6M3NCBTD4RWB3K" , # Prime Video
    "https://www.amazon.in/gp/help/customer/display.html/ref=hp_left_v4_sib?ie=UTF8&nodeId=GQVGZEEUCPK9U5AT#GUID-99183F90-B254-4C9C-A617-22B98153235F__SECTION_ABA6925A71854D41B43915A3B90C0CA7" , # Prime Music 
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=G202159280" , # Prime Deals and Offers 
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GJUW2A8B4X2R4HT7",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GVLCMPJXJ8LE2CTZ",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GDYRXRKS8NUT3D3W",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GMEPD5NLAENJEC9H",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202135170",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GRX62PFZCZLJETJH",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202169540",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202054460",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GFBWMNXEPYVJAY9A",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GTNDYM87YMU7W9CV",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202054820",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GCQ5L4PNEXQH8KYF",
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GF8B8BP3Q4HQADU8",
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GJLLHTPTG32P95DR",
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GSNBBJP63SM65UDB",
    "https://www.amazon.in/gp/help/customer/display.html?nodeId=GECXUKGMDL6SYLH2",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202054800",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G9EAYKPV5YYDB8P7",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G2WRTQ8PRZKGHTB4",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202134240",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=Tnj5Y06X13SOry3D0T",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202210040",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202123460",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G202136010",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GL57MEXDY9RXVF3F",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G5NYX2ESHH6YD6JU",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GFLF3YV4YL26N5Z8",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GQVGZEEUCPK9U5AT",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GQV6LHBN5UZEAQ9C",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GS7MUH4Q24HNJ59Y",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GTXWC3TLMKGJ68HE",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GNYQVR3QCTPTP9CZ",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GDJJB79ANF6LPSTV",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G9NSAWQVKB9KP2C9",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G3AAE2BSVTAEUYUU",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=GT4BFAMD9JJJCMSK",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G2V9QW38TSBLM5U6",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=G2Q4SDFD37T3E892",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=TSOm5057hCkF2SWGJY",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=T2bFwXvwA3nLYBtegQ",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=TXq1xjeKGgiFvGrWmv",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=TBZwF3cpkh8zpQ1dHz",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=TIctMbSCibFXdzifHy",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=TPsdHKyWfsSfQI0NPq",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=Tke5C6jwgr4Uuc6LFd",
    "https://www.amazon.in/gp/help/customer/display.html?ref_=hp_left_v4_sib&nodeId=TZNdZ3dL9Pq8k5rqsq",
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