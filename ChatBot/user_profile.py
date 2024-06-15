import os
from langchain_mistralai import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings
import time
from pinecone import Pinecone as pc
from langchain_pinecone import Pinecone
import env

class user_profile_train:
    def __init__(self, user_profile):
        # Take environment key from the environment
        os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")

        # Initailize the LLM Model
        self.llm = ChatMistralAI(model="mistral-large-latest")
        self.user_profile = user_profile
        self.Index = "customer"
        self.pc = pc(api_key=os.environ.get("PINECONE_API_KEY"))

    def get_user_profile(self):
        index = self.pc.Index(self.Index)

        vectorstore = Pinecone(index, embedding=MistralAIEmbeddings())
        retriever = vectorstore.as_retriever(k=1)

        # Constructing the query based on user profile details
        query_conditions = []

        # Handle Subscription status
        if self.user_profile["Subscription Status"] == "No":
            query_conditions.append("Subscription Status: No")
        else:
            query_conditions.append("Subscription Status: Prime Member")

        # Add age condition
        if "Age" in self.user_profile:
            query_conditions.append(f"Age: {self.user_profile['Age']}")

        # Add location condition
        if "Location" in self.user_profile:
            query_conditions.append(f"Location: {self.user_profile['Location']}")

        # Add visit frequency condition
        if "Visit Frequency" in self.user_profile:
            query_conditions.append(f"Visit Frequency: {self.user_profile['Visit Frequency']}")

        # Add purchase frequency condition
        if "Purchase Frequency" in self.user_profile:
            query_conditions.append(f"Purchase Frequency: {self.user_profile['Purchase Frequency']}")

        # Add preferred payment methods condition
        if "Preferred Payment Methods" in self.user_profile:
            query_conditions.append(f"Preferred Payment Methods: {', '.join(self.user_profile['Preferred Payment Methods'])}")

        # Combine all query conditions
        query = ', '.join(query_conditions)

        # Use the retriever to perform similarity search
        docs = retriever.invoke(query)

        user_needs = []
        # Display the retrieved documents
        for doc in range(len(docs)-1, 0, -1):
            content = docs[doc].page_content
            # print(docs[doc].p_content.Needs)
            needs_start = content.find("Needs: ") + len("Needs: ")
            needs_section = content[needs_start:].strip()

            # Splitting the needs into a list
            needs_list = [need.strip() for need in needs_section.split(",")]
            
            # listing all the user needs 
            user_needs.extend(needs_list)
        
        return user_needs