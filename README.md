# Amazon-HackOn

### For Login you can use email_id: rishav@gmail.com

# Local Setup
```{bash}
git clone --branch test --single-branch https://github.com/Ris-code/Amazon-HackOn.git 
```
```{bash}
cd Amazon-HackOn 
```
```{bash}
pipenv shell 
```
```{bash}
pipenv install 
```
```{bash}
streamlit run app.py 
```

Store the secrets by creating ```secrets.toml``` in ```.streamlit``` directory. Keep all API keys in it.

```{bash}
MISTRAL_API_KEY = ""
PINECONE_API_KEY = ""
HF_TOKEN = ""
MONGO_CONNECTION_STRING = ""
```

## Code References

- Quickstart: https://python.langchain.com/v0.1/docs/use_cases/chatbots/quickstart/
- Memory Management: https://python.langchain.com/v0.1/docs/use_cases/chatbots/memory_management/
- Retrieval: https://python.langchain.com/v0.1/docs/use_cases/chatbots/retrieval/
- Tool Usage: https://python.langchain.com/v0.1/docs/use_cases/chatbots/tool_usage/
- Conversational RAG: https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/
- Build an Agent: https://python.langchain.com/v0.2/docs/tutorials/agents/
- Q&A over SQL+CSV: https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/
- Tool Functioning: https://python.langchain.com/v0.1/docs/modules/model_io/chat/function_calling/

RAG Implementation : https://colab.research.google.com/github/pinecone-io/examples/blob/master/learn/generation/langchain/rag-chatbot.ipynb

## Datasets
https://www.kaggle.com/datasets/shriyashjagtap/e-commerce-customer-for-behavior-analysis?select=ecommerce_customer_data_custom_ratios.csv

https://www.kaggle.com/datasets/mervemenekse/ecommerce-dataset

https://www.kaggle.com/datasets/hassaneskikri/fictional-e-commerce-sales-data
