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
        user = []
        # Display the retrieved documents
        for doc in range(len(docs)-1, 0, -1):
            content = docs[doc].page_content
            # print(docs[doc].p_content.Needs)
            needs_start = content.find("Needs: ") + len("Needs: ")
            needs_section = content[needs_start:].strip()

            # Splitting the needs into a list
            needs_list = [need.strip() for need in needs_section.split(",")]
            
            user_start = content.find("User Type: ") + len("User Type: ")
            start = content.find("\n")

            # print(user_start)
            # print(start)
            user_section = content[user_start:start]
            # print(user_section)
            
            user.append(user_section)
            # listing all the user needs 
            user_needs.extend(needs_list)
        # print(user)
        
        return user_needs, user
    
def fetch_user_attributes(id: str):
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


    user_attributes = [f"{key}: {value}" for key, value in user_profile.items()]
    user_needs, user_type = user_profile_train(user_profile).get_user_profile()

    return user_needs, user_attributes, user_type, user_profile["Name"]