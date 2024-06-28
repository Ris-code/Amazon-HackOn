import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from langchain_mistralai import ChatMistralAI
from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import PromptTemplate
from env import *
from user_profile import *
from tools import tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

# Initialize language model
llm = ChatMistralAI(model="mistral-large-latest")

# Bind the tool to the model
llm = llm.bind_tools(tool)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Define agent
agent = create_tool_calling_agent(llm, tool, hub.pull("hwchase17/openai-functions-agent"))
agent_executor = AgentExecutor(agent=agent, tools=tool)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

async def async_agent_call(user_needs, user_attributes, user_type, question):
    def create_prompt_template():
        template = """
        As an Amazon customer service agent, your primary responsibility is to resolve all payment-related issues for customers.

        **Instructions**:
        - Activate the 'payment_query_search' tool to fetch accurate and relevant information for any payment-related query.
        - Use the 'Amazon_policy' tool to answer questions about Amazon policies.
        - Use 'Amazon-Pay-Services-Faqs' tool for all the questions related to amazon pay services.
        - Use the tool 'Amazon-Pay-Services' for the queries related to Amazon Pay provided services.
        - Use 'Amazon-AWS-Billing-FAQs' tool for the queries related to billings and payments in Amazon web services (AWS).
        - For order confirmations, request the transaction ID and use the 'order_confirmation' tool.
        - If the transaction ID is not found respond as order is not yet confirmed and give assurance to the customer.
        - For Amazon Pay related queries use the tool 'Amazon-Pay-FAQs'.
        - For queries related to financial data, use the 'financial_management' tool.
        - Utilize the 'Customer-pain-point' tool to gauge the seriousness and emotions of the customer and respond accordingly.
        - Utilize the 'Prime-Members' tool to answer the questions about Amazon Prime Membership , queries and subscriptions.

        **Prompt Structure**:
        ```
        Question: {question}
        Note: Use the user profile to understand the user. Here is the profile: {profile}. Focus on solutions and recommendations based on the user's needs: {needs} and use tool "Amazon-Pay-Services".
        ```
        **Response Guidelines**:
        - Tailor responses based on the user's profile.
        - Provide clear, concise, and helpful information.
        - Structure responses with bullet points for clarity and ease of reading.
        - Keep conversations brief and to the point.
        - Format text with clear spacing to ensure readability.
        - Highlight important informations and requirements.
        - Do not mention user types or tools used in the response.

        **Important** : Remember to exclude any tool invocation commands from the response text. Focus solely on providing a helpful and informative reply to the user.
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
    formatted_prompt = format_prompt(prompt_template, question, user_attributes, user_needs, user_type)

    # Asynchronously invoke the agent
    response = await asyncio.to_thread(agent_with_chat_history.invoke, {"input": formatted_prompt}, {"configurable": {"session_id": "<foo>"}})

    return response['output']