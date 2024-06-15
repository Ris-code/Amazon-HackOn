import os
from langchain_mistralai import ChatMistralAI
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import env

def document_split(data):
    # Initialize an empty list to store Document objects
    documents = []

    # Convert dictionaries to Document objects
    for category, questions in data.items():
        content = f"Category: {category}\nQuestions:\n"
        content += "\n".join([f"- {question}" for question in questions])

        metadata = {"category": category}
        documents.append(Document(page_content=content, metadata=metadata))

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Split documents into chunks
    all_splits = text_splitter.split_documents(documents)

    return all_splits

def pinecone_vector_store(data):
    index_name = "query-category"  
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

    docs = document_split(data)

    PineconeVectorStore.from_documents(docs, embedding=MistralAIEmbeddings(), index_name=index_name)

query_category = {
    "Payment Failure": [
        "Why did my payment fail?",
        "Can you help me with a payment failure issue?",
        "What are the common reasons for payment failure?",
        "How can I retry a failed payment?",
        "What should I do if my payment keeps failing?",
        "Is there a way to ensure my payment goes through successfully?",
        "Why is my credit card being declined?",
        "How can I resolve a payment processing error?"
    ],
    "Order Confirmation": [
        "When will I receive my order confirmation?",
        "Why haven't I received an order confirmation email yet?",
        "How long does it take to get an order confirmation?",
        "Can I check the status of my order confirmation online?",
        "What should I do if I don't get an order confirmation email?",
        "Is there a way to resend the order confirmation email?",
        "My order confirmation is missing some details; what should I do?"
    ],
    "Delayed Refunds": [
        "Why is my refund taking so long?",
        "When can I expect to receive my refund?",
        "What should I do if my refund is delayed?",
        "How long does it usually take to process a refund?",
        "Can you expedite my refund process?",
        "What are the steps to check the status of my refund?",
        "My refund hasn't appeared in my account yet; what should I do?"
    ],
    "Security Concern": [
        "How secure is my payment information?",
        "What measures are in place to protect my payment details?",
        "I suspect a security breach; what should I do?",
        "How can I ensure my payment is secure?",
        "Are my credit card details safe on your platform?",
        "What should I do if I notice unauthorized transactions?",
        "How can I report a security concern related to my payment?"
    ],
    "International Payments": [
        "Can I make an international payment?",
        "What are the fees for international payments?",
        "How do I make a payment from abroad?",
        "Are there any restrictions on international payments?",
        "How long do international payments take to process?",
        "What currencies are supported for international payments?",
        "Why is my international payment not going through?"
    ],
    "Hidden Fees": [
        "Are there any hidden fees I should be aware of?",
        "Why was I charged an additional fee?",
        "How can I find out about all the fees associated with my payment?",
        "Can you explain the extra charges on my bill?",
        "How can I avoid hidden fees?",
        "What are the common hidden fees in my transactions?",
        "Why is there a discrepancy between the amount I paid and the amount charged?"
    ],
    "Transaction Limit": [
        "What is the maximum transaction limit?",
        "Can I increase my transaction limit?",
        "Why was my transaction declined due to a limit?",
        "How can I check my current transaction limit?",
        "Are there different limits for different payment methods?",
        "What should I do if I need to make a payment above my limit?",
        "How often are transaction limits updated?"
    ],
    "Loyalty Points and Gift Cards": [
        "How can I redeem my loyalty points?",
        "Can I use multiple gift cards for a single purchase?",
        "How do I check my loyalty points balance?",
        "What can I purchase with my gift cards?",
        "Are there any restrictions on using loyalty points?",
        "How long are gift cards valid for?",
        "Why can't I apply my loyalty points at checkout?"
    ],
    "Promo Codes and Discount Issues": [
        "Why isn't my promo code working?",
        "How can I apply a promo code to my purchase?",
        "Can I use more than one promo code at a time?",
        "What should I do if my discount wasn't applied?",
        "Are there any restrictions on using promo codes?",
        "How do I find available promo codes and discounts?",
        "Why was my promo code rejected?"
    ],
    "Complex Checkout Process": [
        "Why is the checkout process so complicated?",
        "Can you simplify the steps to complete my purchase?",
        "What information do I need to complete the checkout?",
        "How can I speed up the checkout process?",
        "Why do I need to enter so much information at checkout?",
        "Can I save my details to make checkout faster next time?",
        "What should I do if I get stuck during checkout?"
    ],
    "Payment Options": [
        "What payment methods do you accept?",
        "Can I pay with a credit card?",
        "Is there an option to pay with a mobile wallet?",
        "How can I add a new payment method?",
        "Are there any payment methods that offer discounts?",
        "Can I split my payment across multiple methods?",
        "Why isn't my preferred payment option available?"
    ],
    "EMI & Installments": [
        "Do you offer EMI or installment payment options?",
        "How can I choose to pay in installments?",
        "What are the terms and conditions for EMI payments?",
        "Is there any interest on installment payments?",
        "Can I pay off my EMI early?",
        "How do I check the remaining balance on my installment plan?",
        "Why was my EMI request declined?"
    ],
    "Confusing Payment Options": [
        "How do I select the best payment option for me?",
        "What are the differences between the payment options available?",
        "Can you explain the benefits of each payment method?",
        "Why are there so many payment options?",
        "How can I change my selected payment option?",
        "Which payment option is the most secure?",
        "Why is my preferred payment option not recommended?"
    ]
}

pinecone_vector_store(query_category)
