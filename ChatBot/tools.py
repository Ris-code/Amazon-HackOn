import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from pinecone import Pinecone as pc
from langchain_pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from tqdm.autonotebook import tqdm
from langchain_core.tools import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.messages import HumanMessage
from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import PromptTemplate
from env import *
from user_profile import *
import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent

def retrieve_tool(index, topic, description, pinecone_key=os.environ.get("PINECONE_API_KEY")):
    # Initialize Pinecone client
    pc_client = pc(api_key=pinecone_key)
    Index = pc_client.Index(index)

    # Initialize vector store
    vectorstore = Pinecone(Index, embedding=MistralAIEmbeddings())
    retriever = vectorstore.as_retriever(k=1)

    # Create and return the retriever tool
    retriever_tool = create_retriever_tool(
        retriever,
        topic,
        description
    )

    return retriever_tool

## Tool 1
retrieve_tool_1 = retrieve_tool("query-category-new", 
                                topic="payment_query_search", 
                                description="Search for information related to payment queries. For any questions about Payment and payment methods, you must use this tool!",
                                )

## Tool 2
retrieve_tool_2 = retrieve_tool("policy", 
                                topic="Amazon_policy", 
                                description = "Search for amazon policies on payment REFUND, RETURN, REPLACEMENT, PRIVACY_NOTICE, CONDITION_OF_USE, SAFE_ONLINE_SHOPPING, AMAZON_PAY_SAFETY, CHECK_REFUND_STATUS, SECURITY_AND_PRIVACY, RETURN_PICKUP&SELF-SHIP_GUIDELINE, DAMAGE_DEFECTIVE_WRONG_PRODUCT_FAQ, SHIPPING_SPEED&CHARGES, GUARANTEED_SHIPPING_SPEEDSAND_CHARGES, POD, EMI, ACCEPTED_PAYMENT_METHODS, PAYMENT_ISSUES, RESOLVE_DECLINED_PAYMENT, AMAZON_PAY_LATER, TERM_AND_CONDITIONS, PAYMENT_PRICING_PROMOTION, UPI, AMAZON_PAY, AMAZON_PAY_BALANCE, NET_BANKING "
                                )
## Tool 3
retrieve_tool_3 = retrieve_tool("pain-category", 
                                topic="Customer-pain-point", 
                                description = "Understand the pain of customer and the importance of the query. Using these parameters generate proper judgement for the users"
                                )
## Tool 4
retrieve_tool_4 = retrieve_tool("amazon-pay-faqs",
                                topic = "Amazon-Pay-FAQs",
                                description = "Search for amazon pay related questions",
                                pinecone_key=PINECONE_API_KEY_ACCOUNT_2
                                )
## Tool 5
retrieve_tool_5 = retrieve_tool("amazon-services",
                                topic = "Amazon-Pay-Services",
                                description = "Amazon Pay provides various services like SMART STORES, CAR AND BIKE INSURANCE, TRAVEL TICKET BOOKINGS, AMAZON PAY UPI, AMAZON LATER PAY, SMALL AND MEDIUM BUSINESS OWNERS USE AMAZON PAY to ease the life of customers as aell as the merchants",
                                pinecone_key=PINECONE_API_KEY_ACCOUNT_2
                                )
## Tool 6
retrieve_tool_6 = retrieve_tool("prime-info", 
                                topic= "Prime-Members",
                                description= "Search for comprehensive information related to Amazon Prime membership, including benefits such as Prime Video, Prime Music, Prime Reading, shipping benefits, eligible items, promotional codes, terms and conditions, membership management, fees, recurring payments, and FAQs. This tool covers all aspects of Amazon Prime to help users understand and manage their Prime membership effectively.",
                                pinecone_key=PINECONE_API_KEY_ASHU
                                )
## Tool 7
retrieve_tool_7 = retrieve_tool("amazon-pay-services-faqs", 
                                topic= "Amazon-Pay-Services-Faqs",
                                description= """Solve the Amazon Pay related issues like Amazon Pay Flights: MakeMyTrip
                                                Amazon Pay Flights: MakeMyTrip: Terms & Conditions,
                                                Acko Insurance Terms and Conditions,
                                                Bill Payments & Recharges,
                                                Bus Tickets on Amazon,
                                                Movie Ticket Booking on Amazon,
                                                Train Ticket Booking on Amazon,
                                                Amazon Pay Gift Cards,
                                                Amazon Pay Wallet - FAQs,
                                                Amazon Pay KYC FAQs,
                                                Amazon Pay Cashback Offer - FAQs,
                                                EMI (Easy Monthly Installments),
                                                Reporting unauthorized transactions for Amazon Pay Wallet,
                                                Customer Grievance Redressal Policy for Amazon Pay Wallet,
                                                Merchant Grievance Redressal Policy for Amazon Pay,
                                                Auto Reload Amazon Pay Wallet Recurring Payments - Terms & Conditions,
                                                Terms and Conditions - Amazon Pay Wallet,
                                                Amazon Pay Privacy Notice,
                                                Digital Gold - Frequently Asked Questions,
                                                Auto Insurance on Amazon Pay,
                                                Insurance Terms and Conditions,
                                                Google Play recharges,
                                                App Store Code: FAQs,
                                                Metro Smart Card Recharges,
                                                Metro Recharge Terms and Conditions,
                                                Common Gift Card Scams,
                                                Check CIBIL Score,
                                                Subscriptions for Amazon Pay - FAQs,
                                                Service Payments on Amazon.in Terms & Conditions,
                                                Amazon Vouchers,
                                                Amazon Shopping voucher Terms and Conditions,
                                                Wealth – FD & Mutual Funds on Amazon Pay,
                                                Integrated Ombudsman Scheme, 2021: Salient Features,
                                                Amazon Pay Hotels: MakeMyTrip,
                                                Close or Unblock Amazon Pay Later Account,
                                                How to Register with Amazon Pay Later,
                                                How to use Amazon Pay Later,
                                                Amazon Pay Later - Returns and Cancellation,
                                                Amazon Pay Later Repayments,
                                                Amazon Pay Later - Customer Care,
                                                Metro QR Ticketing FAQ,
                                                Accepted Payment Methods,
                                                OTP Issues,
                                                About Pay on Delivery,
                                                About Amazon Pay ICICI Bank Credit Card,
                                                Payment Issues and Restrictions,
                                                Easy Monthly Installments (EMI),
                                                Net Banking,
                                                Price Matching,
                                                Bill Payments,
                                                LPG Cylinder Payments,
                                                Insurance Premium Payments,
                                                Credit Card Bill Payments,
                                                FASTag Recharge,
                                                DTH Recharges,
                                                Google Play recharges,
                                                Prepaid Mobile Recharges""",
                                pinecone_key=PINECONE_API_KEY_ACCOUNT_2
                                )
## tool 8
retrieve_tool_8 = retrieve_tool("amazon-aws-billing-faqs",
                                topic = "Amazon-AWS-Billing-FAQs",
                                description= """Solve the Amazon AWS Billing issues like 
                                What is AWS Billing and Cost Management?,
                                Getting set up with Billing,
                                Setting up your tax information,
                                Customizing your Billing preferences,
                                Customizing your AWS payment preferences,
                                Setting up your India billing,
                                Finding the seller of record,
                                Reviewing your monthly billing best practices,
                                Getting help with your bills and payments,
                                Using the console home page,
                                Knowing the differences between Billing and Cost Explorer data,
                                Understanding your bill,
                                Understanding unexpected charges,
                                Managing your payments,
                                Manage payment access using tags,
                                Make payments, check funds, and view payment history,
                                Managing your payment verifications,
                                Managing credit card and ACH direct debit,
                                Using Advance Pay,
                                Making payments in Chinese yuan,
                                Making payments using PIX (Brazil),
                                Managing your payments in India,
                                Managing your payments in AWS Europe,
                                Making payments, checking unapplied funds, and viewing your payment history in AWS Europe,
                                Managing your AWS Europe credit card payment methods,
                                Managing your AWS Europe credit card payment verifications,
                                Managing your SEPA direct debit payment method,
                                Using payment profiles,
                                Applying AWS credits,
                                Managing your purchase orders,
                                Setting up purchase order configurations,
                                Adding a purchase order,
                                Editing your purchase orders,
                                Deleting your purchase orders,
                                Viewing your purchase orders,
                                Reading your purchase order details page,
                                Enabling purchase order notifications,
                                Use tags to manage access to purchase orders,
                                Trying services using AWS Free Tier,
                                Confirming eligibility to use AWS Free Tier,
                                Avoiding unexpected charges after Free Tier,
                                Track your usage,
                                Using the Free Tier API,
                                Viewing your carbon footprint,
                                Understanding the customer carbon footprint tool,
                                Understanding your carbon emission estimations,
                                Organizing costs using AWS Cost Categories,
                                Creating cost categories,
                                Tagging cost categories,
                                Viewing cost categories,
                                Editing cost categories,
                                Deleting cost categories,
                                Splitting charges within cost categories,
                                Organizing and tracking costs using AWS cost allocation tags,
                                Using AWS-generated tags,
                                Activating AWS-generated tags cost allocation tags,
                                Deactivating the AWS-generated tags cost allocation tags,
                                Using user-defined cost allocation tags,
                                Activating user-defined cost allocation tags,
                                Backfill cost allocation tags,
                                Using the monthly cost allocation report,
                                Understanding dates for cost allocation tags,
                                Calling AWS services and prices using the AWS Price List,
                                Finding services and products,
                                Getting price list files,
                                Get price list files manually,
                                Step 1: Find available AWS services,
                                Step 2: Find available versions for an AWS service,
                                Step 3: Find available AWS Regions for a version of a service,
                                Step 4: Find available price lists for a Region and version of an AWS service,
                                Read the price list files,
                                Read the service index file,
                                Read the service version index file,
                                Service version index file for an AWS service,
                                Service version index file for Savings Plan,
                                Read the service Region index file,
                                Service Region index file for AWS services,
                                Service Region index file for Savings Plan,
                                Read the service price list files,
                                Read the service price list file for an AWS service,
                                Read the service price list file for a Savings Plan,
                                Find prices in the service price list file,
                                Set up price update notifications,
                                Consolidating billing for AWS Organizations,
                                Consolidated billing process,
                                Consolidated billing in AWS EMEA,
                                Consolidated billing in India,
                                Effective billing date, account activity, and volume discounts,
                                Reserved Instances,
                                Billing examples for specific services,
                                Reserved Instances and Savings Plans discount sharing,
                                Understanding Consolidated Bills,
                                Requesting shorter PDF invoices,
                                Organization support charges,
                                Security,
                                Data protection,
                                Identity and Access Management,
                                Overview of managing access,
                                How AWS Billing works with IAM,
                                Identity-based policy with Billing,
                                AWS Billing policy examples,
                                Migrating access control,
                                Bulk migrating your policies,
                                Using the AWS recommended actions,
                                Customizing your fine-grained actions,
                                Rollingback to legacy actions,
                                How to use the affected policies tool,
                                Use scripts to bulk migrate your policies to use fine-grained IAM actions,
                                Mapping fine-grained IAM actions reference,
                                AWS managed policies,
                                Troubleshooting""",
                                pinecone_key=PINECONE_API_KEY_ACCOUNT_2
                            )
@tool
def order_confirmation(transaction_id: str):
    """
    Check if the given transaction ID is present in the user's previous orders.

    Args:
    transaction_id (str): The transaction ID to check.

    Returns:
    tuple: A tuple containing the order details and a confirmation message if the transaction ID is found.
    str: A message indicating that the order is not yet confirmed if the transaction ID is not found.
    """
    user = st.session_state.user
    orders = user['previous_orders']

    for order in orders:
        if order["Transaction ID"] == transaction_id:
            return order, "Your order is confirmed"
    
    return "Your order is not yet confirmed, please wait"

@tool
def financial_management(question: str):
    """
    Fetch the user's financial data based on the provided question.

    This tool interacts with the SQL tool to retrieve financial information such as 
    user spendings on different item categories and savings details. The data includes 
    order details such as Order ID, Product Name, Product Category, MRP, Price for 
    Customer, Savings, Payment Method, Monthly Payment, Duration (months), Order Date, 
    and Order Month.

    Args:
    question (str): The financial management question to query the SQL tool with.

    Returns:
    str: The output result from the SQL tool based on the input question.
    """
    llm = ChatMistralAI(model="mistral-large-latest")

    data_path = os.path.join(os.path.dirname(__file__), '..', 'Automated Budgeting Solution', 'customer_orders.csv')
    df = pd.read_csv(data_path)

    engine = create_engine("sqlite:///customer_orders.db")
    df.to_sql("customer_order", engine, index=False)
    db = SQLDatabase(engine=engine)

    sql_tool = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)
    
    result = sql_tool.invoke({"input": question})
    return result['output']


tool = [retrieve_tool_1, 
        retrieve_tool_2, 
        retrieve_tool_3, 
        retrieve_tool_4, 
        retrieve_tool_5,
        retrieve_tool_6,
        retrieve_tool_7,
        retrieve_tool_8,
        order_confirmation, 
        financial_management]