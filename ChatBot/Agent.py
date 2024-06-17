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
from tools import tool

# Load environment variables
load_dotenv()

# Initialize language model
llm = ChatMistralAI(model="mistral-large-latest")

# Define user profile
user_profile = {
    "Name": "Rishav",
    "Age": 20,
    "Gender": "Male",
    "Location": "Noida, UP",
    "Account Age": "3 years",
    "Visit Frequency": "5 visits in the last 10 days",
    "Purchase Frequency": "2 purchases in the last month",
    "Average Purchase Value": "$1000 per purchase",
    "Cart Abandonment Rate": "3 abandoned carts in the last month",
    "Engagement with Promotions": "Clicked on 3 promotional emails in the last month",
    "Wishlist Activity": "Added 5 items to wishlist in the last month",
    "Browsing History": ["Laptops", "Smartphones", "Books"],
    "Subscription Status": "No",
    "Preferred Payment Methods": ["Credit Card", "Mobile Wallet", "Amazon Pay", "UPI", "Debit Card"]
}

def get_profile(user_profile):
    user_attributes = [f"{key}: {value}" for key, value in user_profile.items()]
    user_needs, user_type = user_profile_train(user_profile).get_user_profile()

    return user_needs, user_attributes, user_type

user_needs, user_attributes, user_type = get_profile(user_profile)

# Bind the tool to the model
llm = llm.bind_tools(tool)

def create_prompt_template():
    template = """
    As an Amazon customer service agent, your primary responsibility is to resolve all payment-related issues for customers. You have access to a specialized tool called 'payment_query_search,' which is designed to provide information regarding payment errors, methods, or processes. Whenever a user approaches you with a query related to payments, activate the 'payment_query_search' tool to fetch accurate and relevant information. You also need to carefully consider the 'Amazon_policy' tool to answer the user question.

    Here is the prompt structure you should follow when responding to payment-related queries:
    ```
    question: {question}
    Note: Use the user profile to understand the user. Here is the profile: {profile}. Focus on the solutions and recommendations based on the user's needs: {needs}.
    ```

    Remember to tailor your responses based on the user's profile and provide clear and helpful information to assist them effectively in resolving their payment issues. Its better to provide the solutions in points to improve user experience.

    The user type is {user_type}. Do not mention it in the response. Just use this to understand the user sentiment for a better solution.

    Do not mention the tools used to solve the issue or explicitly state the user type in the response.
    """
    return PromptTemplate.from_template(template=template)

def format_prompt(prompt_template, question, users, needs, types):
    users_str = "\n".join(users)
    needs_str = "\n".join(needs)
    types_str = "\n".join(types)
    return prompt_template.format(
        question=question,
        profile = users_str,
        user_type=types_str,
        needs=needs_str
    )

# Prepare the prompt
prompt_template = create_prompt_template()
formatted_prompt = format_prompt(prompt_template, "Why there is delay in my refund?", user_attributes, user_needs, user_type)

# Define agent
agent = create_tool_calling_agent(llm, tool, hub.pull("hwchase17/openai-functions-agent"))
agent_executor = AgentExecutor(agent=agent, tools=tool)

# Invoke the agent with the formatted prompt
response = agent_executor.invoke({"input": formatted_prompt})
print(response['output'])
