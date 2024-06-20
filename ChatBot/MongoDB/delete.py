from pymongo import MongoClient
import os
from dotenv import load_dotenv
import uuid
import random

load_dotenv()
# Assuming you have connected to your MongoDB server
client = MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
db = client["amazon"]
collection = db["user_profiles"]

# Delete all documents from the collection
result = collection.delete_many({})
# Print the number of documents deleted
print(f"Deleted {result.deleted_count} documents from the collection")
