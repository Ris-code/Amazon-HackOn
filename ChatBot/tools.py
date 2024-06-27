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
        order_confirmation, 
        financial_management]