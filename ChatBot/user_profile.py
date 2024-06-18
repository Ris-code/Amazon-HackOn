from pinecone import Pinecone as pc
from langchain_pinecone import Pinecone
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
import os

class UserProfileTrainer:
    def __init__(self, user_profile):
        self.llm = ChatMistralAI(model="mistral-large-latest")
        self.user_profile = user_profile
        self.index = "customer"
        self.pc = pc(api_key=os.getenv("PINECONE_API_KEY"))

    def get_user_profile(self):
        index = self.pc.Index(self.index)
        vectorstore = Pinecone(index, embedding=MistralAIEmbeddings())
        retriever = vectorstore.as_retriever(k=1)

        # Define profile attributes and query conditions
        profile_attributes = {
            "Subscription Status": f"Subscription Status: {self.user_profile.get('Subscription Status', 'No')}",
            "Age": f"Age: {self.user_profile.get('Age', '')}",
            "Location": f"Location: {self.user_profile.get('Location', '')}",
            "Visit Frequency": f"Visit Frequency: {self.user_profile.get('Visit Frequency', '')}",
            "Purchase Frequency": f"Purchase Frequency: {self.user_profile.get('Purchase Frequency', '')}",
            "Preferred Payment Methods": f"Preferred Payment Methods: {', '.join(self.user_profile.get('Preferred Payment Methods', []))}"
        }

        # Constructing the query based on user profile details
        query = ', '.join(filter(None, profile_attributes.values()))

        # Use the retriever to perform similarity search
        docs = retriever.invoke(query)

        user_needs = []
        user_type = []

        # Extract user needs and type from retrieved documents
        for doc in range(len(docs) - 1, 0, -1):
            content = docs[doc].page_content
            needs_start = content.find("Needs: ") + len("Needs: ")
            needs_section = content[needs_start:].strip()

            # Splitting the needs into a list
            needs_list = [need.strip() for need in needs_section.split(",")]

            user_start = content.find("User Type: ") + len("User Type: ")
            start = content.find("\n")

            user_section = content[user_start:start].strip()

            user_type.append(user_section)
            user_needs.extend(needs_list)

        return user_needs, user_type

def fetch_user_attributes(user_profile):
    user_attributes = [f"{key}: {value}" for key, value in user_profile.items()]
    user_needs, user_type = UserProfileTrainer(user_profile).get_user_profile()
    return user_needs, user_attributes, user_type, user_profile.get("Name", "")
