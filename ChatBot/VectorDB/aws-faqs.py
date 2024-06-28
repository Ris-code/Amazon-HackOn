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
    index_name = "amazon-aws-billing-faqs"
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
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-getting-started.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-account-payment.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-pref.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-payment-method.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-account-payment-aispl.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/finding-the-seller-of-record.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/monthly-billing-checklist.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-get-answers.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/view-billing-dashboard.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/differences-billing-data-cost-explorer-data.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/getting-viewing-bill.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/checklistforunwantedcharges.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-payments.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-payments-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-making-a-payment.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cc-verification.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cc.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-advancepay.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-payment-cny.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-payment-brazil.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/edit-aispl-payment-method.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/emea-payments.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-making-a-payment-emea.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cc-emea.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-emea-cc-verification.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-debit-emea.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-paymentprofiles.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-paymentprofiles.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-purchaseorders.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/setup-po-lineitem.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/adding-po.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/edit-po.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/delete-po.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/viewing-po.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/reading-po-details.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/notify-po-details.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-access-to-purchase-orders-with-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-free-tier.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-eligibility.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/avoid-charges-after-free-tier.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-free-tier-api.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ccft-overview.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ccft-estimation.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cost-categories.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/create-cost-categories.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tag-cost-categories.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/view-cost-categories.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/edit-cost-categories.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/delete-cost-categories.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/splitcharge-cost-categories.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/aws-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activate-built-in-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/deactivate-built-in-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/custom-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-allocation-backfill.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/configurecostallocreport.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-allocation-tags-timeline.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-price-list-query-api.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-the-aws-price-list-bulk-api.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-procedure.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing-emea.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-India.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-effective.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidatedbilling-other.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-turn-off.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/con-bill-blended-rates.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-invoice-summary-options.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidatedbilling-support.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/security.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/data-protection.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/security-iam.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/control-access-billing.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/security_iam_service-with-iam.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/security_iam_id-based-policy-examples.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-example-policies.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-granularaccess-whatis.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-granularaccess-console.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-console-streamlined.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-console-customized.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-console-rollback.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-security-iam-tool.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-iam-permissions.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/migrate-granularaccess-iam-mapping-reference.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/managed-policies.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/security_iam_troubleshoot.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-the-aws-price-list-bulk-api-fetching-price-list-files-manually.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/fetching-price-list-manually-step-1.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/fetching-price-list-files-manually-step-2.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/fetching-price-list-files-manually-step-3.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/fetching-price-list-files-manually-step-4.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/bulk-api-reading-price-list-files.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/reading-service-index-files.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-the-aws-price-list-bulk-api-reading-price-list-files-reading-service-version-index-file.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/service-version-index-file-for-aws-service.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/service-version-index-file-for-savings-plans.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/reading-service-region-index-files.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/service-region-infex-file-for-service.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/service-region-index-files-for-savings-plan.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/reading-service-price-list-files.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/reading-service-price-list-file-for-services.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/reading-service-price-list-file-for-savings-plans.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/finding-prices-in-service-price-list-files.html" ,
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/notifications-price-list-api.html" ,
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
    # print(cleaned_documents)

    for i in split_documents:
    # # Process and store each chunk in Pinecone
        pinecone_vector_store([i])