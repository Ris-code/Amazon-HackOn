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
# os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY_ACCOUNT_2")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

def document_split(faqs):
    # Initialize an empty list to store Document objects
    documents = []

    # Convert FAQs to Document objects
    for faq in faqs:
        content = f"Question: {faq['question']}\nAnswer: {faq['answer']}"
        metadata = {
            "question": faq["question"]
        }
        documents.append(Document(page_content=content, metadata=metadata))

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Split documents into chunks
    all_splits = text_splitter.split_documents(documents)

    return all_splits

def pinecone_vector_store(faq):
    index_name = "amazon-pay-faqs"  
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

    docs = document_split(faq)

    PineconeVectorStore.from_documents(docs, embedding=MistralAIEmbeddings(), index_name=index_name)

     

FAQs= [
{
    "question": "What is Amazon Pay?",
    "answer": "Amazon Pay is a service that lets you use the payment methods already associated with your Amazon account to make payments for goods, services, and donations on third-party websites, and in apps. To make a payment, you can use any of the payment methods on file in your Amazon account. Beyond the button, shoppers can manage their payments using Amazon Pay on Amazon.com."
},
{
    "question": "How do I sign up?",
    "answer": "If you already have an account with Amazon, you only have to accept Amazon's Conditions of Use and Privacy Notice when signing in on a non-Amazon site that accepts Amazon Pay. There is no separate registration process."
},
{
    "question": "Am I protected when I use Amazon Pay?",
    "answer": "If there are ever unauthorized Amazon Pay charges in your personal account, you can dispute the charge with us. You must notify us as quickly as possible and no later than 13 months after the date of the transaction. Unless you've acted fraudulently or with negligence, you may not be held responsible for the charge. For more information, see Unauthorized charges.\n\nWhen you use Amazon Pay for qualified purchases on third-party websites, the condition of the item that you buy and its timely delivery may be guaranteed under the Amazon Pay A-to-z Guarantee for Customers. If you submit payment for a product or service and you don't receive the item or if it is materially different than advertised by the merchant, you can dispute the transaction and request reimbursement. For more information, see Buyer Dispute Programme and Transaction disputes."
},
{
    "question": "Is my payment information shared with merchants?",
    "answer": "We don't share your full credit card, debit card, or bank account number with merchants or charitable organizations who accept Amazon Pay. However, we do share your full card or bank account number with payment service providers to process the transaction on behalf of the merchant. We also share with the merchant the payment information that is required to complete and support your transaction, which can include the last four digits of your card number and the card type."
},
{
    "question": "What payment methods can be used with Amazon Pay?",
    "answer": "Amazon Pay accepts credit and debit cards. Credit cards currently accepted include Visa, Mastercard, Discover, American Express, Diners Club, and JCB. The Amazon.com store card is available for use with selected merchants. To learn more, see Accepted payment methods."
},
{
    "question": "What does it cost me to use Amazon Pay?",
    "answer": "It costs you nothing. Using Amazon Pay adds no fees to your transaction with the merchant. Your purchase incurs no transaction fee, no membership fee, no currency conversion fee, no foreign transaction fee, and no other fees. Your card issuer, however, may add a foreign transaction fee if your card was issued in a country different from the merchant's, as well as any other fees described in the terms and conditions for your card."
},
{
    "question": "How do I change my account information?",
    "answer": "You can manage most aspects of your Amazon account for Amazon Pay on the Amazon website. Go to Amazon.com, sign in, and then click Your Account. Other changes must be made on the Amazon Pay website.\n\nFor details about the information that can be changed and where to change it, see Making changes to your Amazon account information for Amazon Pay."
},
{
    "question": "How do I make a payment?",
    "answer": "When you see that Amazon Pay is an accepted payment method for a product or service that you want to purchase, just click the Amazon Pay logo or button, enter your Amazon.com email address and password, and then choose your payment method. For more information about making payments using Amazon Pay, see Using Amazon Pay."
},
{
    "question": "How can I find a payment that I made using Amazon Pay on my credit card statement?",
    "answer": "Payments that you make using Amazon Pay appear on your credit card statement like this:\n\nAMZ*[Seller Name] amzn.com/pmts"
},
{
    "question": "Where can I see a record of my purchases and donations?",
    "answer": "You will receive an email confirmation for each purchase and donation. You can review a history of all your donations and other Amazon Pay transactions at pay.amazon.com. Charitable organizations that you donate to will also provide email receipts for your donations."
},
{
    "question": "How do I find my donation receipt for use as an income tax deduction?",
    "answer": "The charitable organization that you donated to is responsible for giving you the proper tax document. If you haven't received a receipt that is valid for your income tax reporting purposes, contact them directly."
},
{
    "question": "Can I ship my order to an Amazon Locker?",
    "answer": "No, only purchases made directly on the Amazon.com website may ship to an Amazon Locker. Please don't add the address of an Amazon Locker as a shipping address for your Amazon Pay purchases. Orders that are paid for using Amazon Pay cannot be delivered to an Amazon Locker."
},
{
    "question": "I think I just received a phishing email. What do I do?",
    "answer": "If you have received an email that you know is a forgery, or if you think you have been a victim of a phishing attack and you are concerned about your Amazon.com account, please let us know right away by reporting a phishing or spoofed email."
},
{
    "question": "I'm having a problem with my account or with trying to complete a purchase using my account. What do I do?",
    "answer": "We are sorry you are having a problem with Amazon Pay. Here are some things you can try:\n\n1. Verify that you are entering the email address and password that are associated with your Amazon.com account correctly when you are trying to complete a purchase.\n2. If you can enter your account email address and password, but you cannot complete your purchase, check that your payment method is set up correctly. You can do so by following the steps listed in Making changes to your Amazon account information for Amazon Pay.\n3. If your payment method is set up correctly, check that you have updated your browser's settings to allow third-party cookies. If the option is turned on and you still cannot complete your purchase, contact us."
}
]


pinecone_vector_store(FAQs)