import os
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

def retrieve_tool(index, topic, description):
    # Initialize Pinecone client
    pc_client = pc(api_key=os.environ.get("PINECONE_API_KEY"))
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
                                description="Search for information related to payment queries. For any questions about Payment and payment methods, you must use this tool!"
                                )

## Tool 2
retrieve_tool_2 = retrieve_tool("policy", 
                                topic="Amazon_policy", 
                                description = "Search for amazon policies on payment REFUND, RETURN, REPLACEMENT, PRIVACY_NOTICE, CONDITION_OF_USE, SAFE_ONLINE_SHOPPING, AMAZON_PAY_SAFETY, CHECK_REFUND_STATUS, SECURITY_AND_PRIVACY, RETURN_PICKUP&SELF-SHIP_GUIDELINE, DAMAGE_DEFECTIVE_WRONG_PRODUCT_FAQ, SHIPPING_SPEED&CHARGES, GUARANTEED_SHIPPING_SPEEDSAND_CHARGES, POD, EMI, ACCEPTED_PAYMENT_METHODS, PAYMENT_ISSUES, RESOLVE_DECLINED_PAYMENT, AMAZON_PAY_LATER, TERM_AND_CONDITIONS, PAYMENT_PRICING_PROMOTION, UPI, AMAZON_PAY, AMAZON_PAY_BALANCE, NET_BANKING "
                                )

tool = [retrieve_tool_1, retrieve_tool_2]