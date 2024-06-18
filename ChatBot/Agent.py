import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from langchain_mistralai import ChatMistralAI
# from langchain import hub
# from langchain.agents import create_tool_calling_agent
# from langchain.agents import AgentExecutor
# from langchain import PromptTemplate
# from env import *
# from user_profile import *
# from tools import tool
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory

# store = {}

# # Initialize language model
# llm = ChatMistralAI(model="mistral-large-latest")

# # Bind the tool to the model
# llm = llm.bind_tools(tool)

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]

#     # Define agent
# agent = create_tool_calling_agent(llm, tool, hub.pull("hwchase17/openai-functions-agent"))
# agent_executor = AgentExecutor(agent=agent, tools=tool)

# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="chat_history",
# )

# def agent(user_needs, user_attributes, user_type, question):
#     def create_prompt_template():
#         template = """
#         - As an Amazon customer service agent, your primary responsibility is to resolve all payment-related issues for customers. 
#         - You have access to a specialized tool called 'payment_query_search,' which is designed to provide information regarding payment errors, methods, or processes. Whenever a user approaches you with a query related to payments, activate the 'payment_query_search' tool to fetch accurate and relevant information. 
#         - You also need to carefully consider the 'Amazon_policy' tool to answer the user question.
#         - Use the 'Customer-pain-point' tool to understand the seriousness and emotions of the customer. Accordingly make the judgements to generate proper responses to satisfy user emotions.
#         - For any questions other than payment-related queries, respond respectfully indicating that you are a bot designed to solve payment-related queries, and politely ask the user to focus on payment-related issues.
#         - Try to keep the conversations to the point. 
#         - Use proper text formattings to make the responses attractive and interactive.
#         - Format the text with clear spacing which ensures that the text remains readable.
#         - Do not mention the user types in the response.

#         Here is the prompt structure you should follow when responding to payment-related queries:
#         ```
#         question: {question}
#         Note: Use the user profile to understand the user. Here is the profile: {profile}. Focus on the solutions and recommendations based on the user's needs: {needs}.
#         ```
#         Remember:
#         - Tailor your responses based on the user's profile.
#         - Provide clear and helpful information to assist them effectively in resolving their payment issues.
#         - Provide the solutions in points to improve user experience.
#         - Keep the conversations short and to the point.        
#         - The user type is {user_type}. 
#         - Its strictly forbidden to mention the user type in the response. Just use the user types to understand the user sentiment for a better solution.
#         - Do not mention the tools used to solve the issue or explicitly state the user type in the response.

#         """
#         return PromptTemplate.from_template(template=template)

#     def format_prompt(prompt_template, question, users, needs, types):
#         users_str = "\n".join(users)
#         needs_str = "\n".join(needs)
#         types_str = "\n".join(types)
#         return prompt_template.format(
#             question=question,
#             profile = users_str,
#             user_type=types_str,
#             needs=needs_str
#         )

#     # Prepare the prompt
#     prompt_template = create_prompt_template()
#     formatted_prompt = format_prompt(prompt_template, question, user_attributes, user_needs, user_type)


#     response =  agent_with_chat_history.invoke({"input": formatted_prompt},config={"configurable": {"session_id": "<foo>"}},)
#     print(response['chat_history'])
#     # Invoke the agent with the formatted prompt
#     # response = agent_executor.invoke({"input": formatted_prompt})
    
#     return response['output']

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
        - As an Amazon customer service agent, your primary responsibility is to resolve all payment-related issues for customers. 
        - You have access to a specialized tool called 'payment_query_search,' which is designed to provide information regarding payment errors, methods, or processes. Whenever a user approaches you with a query related to payments, activate the 'payment_query_search' tool to fetch accurate and relevant information. 
        - You also need to carefully consider the 'Amazon_policy' tool to answer the user question.
        - Use the 'Customer-pain-point' tool to understand the seriousness and emotions of the customer. Accordingly make the judgements to generate proper responses to satisfy user emotions.
        - For any questions other than payment-related queries, respond respectfully indicating that you are a bot designed to solve payment-related queries, and politely ask the user to focus on payment-related issues.
        - Try to keep the conversations to the point. 
        - Use proper text formattings to make the responses attractive and interactive.
        - Format the text with clear spacing which ensures that the text remains readable.
        - Do not mention the user types in the response.

        Here is the prompt structure you should follow when responding to payment-related queries:
        ```
        question: {question}
        Note: Use the user profile to understand the user. Here is the profile: {profile}. Focus on the solutions and recommendations based on the user's needs: {needs}.
        ```
        Remember:
        - Tailor your responses based on the user's profile.
        - Provide clear and helpful information to assist them effectively in resolving their payment issues.
        - Provide the solutions in points to improve user experience.
        - Keep the conversations short and to the point.        
        - The user type is {user_type}. 
        - Its strictly forbidden to mention the user type in the response. Just use the user types to understand the user sentiment for a better solution.
        - Do not mention the tools used to solve the issue or explicitly state the user type in the response.

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
