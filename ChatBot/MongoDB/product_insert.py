from pymongo import MongoClient
import sys
import os
from dotenv import load_dotenv

load_dotenv()

items = [
    {
        "name": "Raymond Yellow Shirt",
        "price": "Rs 454",
        "image": "https://m.media-amazon.com/images/I/41B+TiDYZRL.jpg",
        "payment_methods": [
            {"method": "Credit Card", "cashback": 10.0, "additional_cost": 0.0},
            {"method": "Debit Card", "cashback": 5.0, "additional_cost": 0.0},
            {"method": "Net Banking", "cashback": 0.0, "additional_cost": 0.0},
            {"method": "Cash on Delivery", "cashback": 0.0, "additional_cost": 20.0},
            {"method": "Amazon Pay", "cashback": 20.0, "additional_cost": 0.0},
            {"method": "UPI", "cashback": 15.0, "additional_cost": 0.0}
        ]
    },
    {
        "name": "Noise Pulse Go",
        "price": "Rs 1,099",
        "image": "https://m.media-amazon.com/images/I/61akt30bJsL._SX679_.jpg",
        "payment_methods": [
            {"method": "Credit Card", "cashback": 15.0, "additional_cost": 0.0},
            {"method": "Debit Card", "cashback": 7.0, "additional_cost": 0.0},
            {"method": "Net Banking", "cashback": 5.0, "additional_cost": 0.0},
            {"method": "Cash on Delivery", "cashback": 0.0, "additional_cost": 25.0},
            {"method": "Amazon Pay", "cashback": 30.0, "additional_cost": 0.0},
            {"method": "UPI", "cashback": 20.0, "additional_cost": 0.0}
        ]
    },
    {
        "name": "Iphone 15 Pro Max",
        "price": "Rs 1,48,000",
        "image": "https://m.media-amazon.com/images/I/61Jrsu9d3-L._SX679_.jpg",
        "payment_methods": [
            {"method": "Credit Card", "cashback": 1000.0, "additional_cost": 0.0},
            {"method": "Debit Card", "cashback": 500.0, "additional_cost": 0.0},
            {"method": "Net Banking", "cashback": 0.0, "additional_cost": 0.0},
            {"method": "Cash on Delivery", "cashback": 0.0, "additional_cost": 100.0},
            {"method": "Amazon Pay", "cashback": 2000.0, "additional_cost": 0.0},
            {"method": "UPI", "cashback": 1500.0, "additional_cost": 0.0}
        ]
    },
    {
        "name": "SPARX Mens Sx0706g",
        "price": "Rs 749",
        "image": "https://m.media-amazon.com/images/I/41BNwMRUaJL._SY695_.jpg",
        "payment_methods": [
            {"method": "Credit Card", "cashback": 8.0, "additional_cost": 0.0},
            {"method": "Debit Card", "cashback": 4.0, "additional_cost": 0.0},
            {"method": "Net Banking", "cashback": 0.0, "additional_cost": 0.0},
            {"method": "Cash on Delivery", "cashback": 0.0, "additional_cost": 15.0},
            {"method": "Amazon Pay", "cashback": 10.0, "additional_cost": 0.0},
            {"method": "UPI", "cashback": 7.0, "additional_cost": 0.0}
        ]
    },
    {
        "name": "ZAVERI PEARLS Necklace",
        "price": "Rs 410",
        "image": "https://m.media-amazon.com/images/I/71eaAiL-wjL._SY695_.jpg",
        "payment_methods": [
            {"method": "Credit Card", "cashback": 6.0, "additional_cost": 0.0},
            {"method": "Debit Card", "cashback": 3.0, "additional_cost": 0.0},
            {"method": "Net Banking", "cashback": 0.0, "additional_cost": 0.0},
            {"method": "Cash on Delivery", "cashback": 0.0, "additional_cost": 10.0},
            {"method": "Amazon Pay", "cashback": 8.0, "additional_cost": 0.0},
            {"method": "UPI", "cashback": 5.0, "additional_cost": 0.0}
        ]
    },
    {
        "name": "Body Maxx 78005 Dumbbell",
        "price": "Rs 1,399",
        "image": "https://m.media-amazon.com/images/I/51cc+xTtHiL._SX679_.jpg",
        "payment_methods": [
            {"method": "Credit Card", "cashback": 20.0, "additional_cost": 0.0},
            {"method": "Debit Card", "cashback": 10.0, "additional_cost": 0.0},
            {"method": "Net Banking", "cashback": 5.0, "additional_cost": 0.0},
            {"method": "Cash on Delivery", "cashback": 0.0, "additional_cost": 30.0},
            {"method": "Amazon Pay", "cashback": 25.0, "additional_cost": 0.0},
            {"method": "UPI", "cashback": 15.0, "additional_cost": 0.0}
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
    add_products(product)
