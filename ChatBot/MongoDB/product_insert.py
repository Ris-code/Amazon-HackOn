from pymongo import MongoClient
import sys
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

items = [
    {
        "name": "Raymond Yellow Shirt",
        "price": "Rs 454",
        "image": "https://m.media-amazon.com/images/I/41B+TiDYZRL.jpg",
        "payment_methods": [
            {"method": "Amazon Pay UPI", "cashback_percentage": 5.0, "additional_cost_percentage": 1.0},
            {"method": "Google Pay", "cashback_percentage": 2.0, "additional_cost_percentage": 0.0},
            {"method": "PhonePe", "cashback_percentage": 4.0, "additional_cost_percentage": 0.0},
            {"method": "Credit Card", "cashback_percentage": 3.0, "additional_cost_percentage": 0.0},
            {"method": "Debit Card", "cashback_percentage": 3.0, "additional_cost_percentage": 0.5},
            {"method": "EMI", "cashback_percentage": 10.0, "additional_cost_percentage": 5.0},
            {"method": "Net Banking", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "Cash on Delivery", "cashback_percentage": 5.0, "additional_cost_percentage": 2.0}
        ]
    },
    {
        "name": "Noise Pulse Go",
        "price": "Rs 1,099",
        "image": "https://m.media-amazon.com/images/I/61akt30bJsL._SX679_.jpg",
        "payment_methods": [
            {"method": "Amazon Pay UPI", "cashback_percentage": 15.0, "additional_cost_percentage": 0.5},
            {"method": "Google Pay", "cashback_percentage": 5.0, "additional_cost_percentage": 0.0},
            {"method": "PhonePe", "cashback_percentage": 30.0, "additional_cost_percentage": 0.0},
            {"method": "Credit Card", "cashback_percentage": 20.0, "additional_cost_percentage": 0.0},
            {"method": "Debit Card", "cashback_percentage": 7.0, "additional_cost_percentage": 0.3},
            {"method": "EMI", "cashback_percentage": 10.0, "additional_cost_percentage": 2.5},
            {"method": "Net Banking", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "Cash on Delivery", "cashback_percentage": 5.0, "additional_cost_percentage": 2.0}
        ]
    },
    {
        "name": "iPhone 15 Pro Max",
        "price": "Rs 1,48,000",
        "image": "https://m.media-amazon.com/images/I/61Jrsu9d3-L._SX679_.jpg",
        "payment_methods": [
            {"method": "Amazon Pay UPI", "cashback_percentage": 20.0, "additional_cost_percentage": 0.8},
            {"method": "Google Pay", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "PhonePe", "cashback_percentage": 13.5, "additional_cost_percentage": 0.0},
            {"method": "Credit Card", "cashback_percentage": 20.0, "additional_cost_percentage": 0.4},
            {"method": "Debit Card", "cashback_percentage": 10.0, "additional_cost_percentage": 0.3},
            {"method": "EMI", "cashback_percentage": 25.0, "additional_cost_percentage": 6.8},
            {"method": "Net Banking", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "Cash on Delivery", "cashback_percentage": 5.0, "additional_cost_percentage": 2.0}
        ]
    },
    {
        "name": "SPARX Mens Sx0706g",
        "price": "Rs 749",
        "image": "https://m.media-amazon.com/images/I/41BNwMRUaJL._SY695_.jpg",
        "payment_methods": [
            {"method": "Amazon Pay UPI", "cashback_percentage": 8.0, "additional_cost_percentage": 0.2},
            {"method": "Google Pay", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "PhonePe", "cashback_percentage": 10.0, "additional_cost_percentage": 0.0},
            {"method": "Credit Card", "cashback_percentage": 7.0, "additional_cost_percentage": 0.0},
            {"method": "Debit Card", "cashback_percentage": 4.0, "additional_cost_percentage": 0.1},
            {"method": "EMI", "cashback_percentage": 20.0, "additional_cost_percentage": 2.145},
            {"method": "Net Banking", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "Cash on Delivery", "cashback_percentage": 5.0, "additional_cost_percentage": 2.0}
        ]
    },
    {
        "name": "ZAVERI PEARLS Necklace",
        "price": "Rs 410",
        "image": "https://m.media-amazon.com/images/I/71eaAiL-wjL._SY695_.jpg",
        "payment_methods": [
            {"method": "Amazon Pay UPI", "cashback_percentage": 6.0, "additional_cost_percentage": 0.1},
            {"method": "Google Pay", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "PhonePe", "cashback_percentage": 8.0, "additional_cost_percentage": 0.0},
            {"method": "Credit Card", "cashback_percentage": 5.0, "additional_cost_percentage": 0.0},
            {"method": "Debit Card", "cashback_percentage": 3.0, "additional_cost_percentage": 0.05},
            {"method": "EMI", "cashback_percentage": 15.0, "additional_cost_percentage": 2.44},
            {"method": "Net Banking", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "Cash on Delivery", "cashback_percentage": 5.0, "additional_cost_percentage": 2.0}
        ]
    },
    {
        "name": "Body Maxx 78005 Dumbbell",
        "price": "Rs 1,399",
        "image": "https://m.media-amazon.com/images/I/51cc+xTtHiL._SX679_.jpg",
        "payment_methods": [
            {"method": "Amazon Pay UPI", "cashback_percentage": 20.0, "additional_cost_percentage": 0.3},
            {"method": "Google Pay", "cashback_percentage": 5.0, "additional_cost_percentage": 0.0},
            {"method": "PhonePe", "cashback_percentage": 25.0, "additional_cost_percentage": 0.0},
            {"method": "Credit Card", "cashback_percentage": 15.0, "additional_cost_percentage": 0.0},
            {"method": "Debit Card", "cashback_percentage": 10.0, "additional_cost_percentage": 0.15},
            {"method": "EMI", "cashback_percentage": 25.0, "additional_cost_percentage": 2.145},
            {"method": "Net Banking", "cashback_percentage": 0.0, "additional_cost_percentage": 0.0},
            {"method": "Cash on Delivery", "cashback_percentage": 5.0, "additional_cost_percentage": 2.0}
        ]
    }
]


# Function to add a user profile to MongoDB
def add_products(product):
    # MongoDB connection details
    client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))  
    db = client['amazon']  
    collection = db['Products']  
    print(collection)
    # Insert the user profile into the MongoDB collection
    collection.insert_one(product)
    print("Products added successfully!")
    
for product in items:
    product['item_id'] = str(uuid.uuid4())  # Add a unique item_id to each product
    add_products(product)
