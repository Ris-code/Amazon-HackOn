from pymongo import MongoClient
import os
from dotenv import load_dotenv
import uuid
import random

load_dotenv()

# Define the user profile schema as a Python dictionary
users = [
    {
        "Name": "Rishav",
        "Age": 20,
        "Gender": "Male",
        "Location": "Noida, UP",
        "Account Age": "3 years",
        "Visit Frequency": "5 visits in the last 10 days",
        "Purchase Frequency": "4 purchases in the last month",
        "Average Purchase Value": "Rs 3000 per purchase",
        "Cart Abandonment Rate": "3 abandoned carts in the last month",
        "Engagement with Promotions": "Clicked on 3 promotional emails in the last month",
        "Wishlist Activity": "Added 5 items to wishlist in the last month",
        "Browsing History": ["Laptops", "Smartphones", "Books"],
        "Subscription Status": "No",
        "Preferred Payment Methods": ["Credit Card", "Amazon Pay", "UPI", "Debit Card"],
        "user_id": "rishav@gmail.com",
        "Previous Orders": [
            {"Item Name": "Laptop", "Cost": "Rs 50,000", "Payment Method": "Credit Card", "Additional Cost": "Rs 2", "Cashback": "Rs 400"},
            {"Item Name": "Smartphone", "Cost": "Rs 20,000", "Payment Method": "Amazon Pay", "Additional Cost": "Rs 0", "Cashback": "Rs 1000"},
            {"Item Name": "Headphones", "Cost": "Rs 5000", "Payment Method": "Debit Card", "Additional Cost": "Rs 100", "Cashback": "Rs 200"},
            {"Item Name": "Fitness Tracker", "Cost": "Rs 3000", "Payment Method": "UPI", "Additional Cost": "Rs 0", "Cashback": "Rs 150"}
        ],
        "payment_usage": [
            {"Payment Method": "Amazon Pay UPI", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Google Pay", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "PhonePe", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Credit Card", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Debit Card", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "EMI", "Usage Count": 0},
            {"Payment Method": "Net Banking", "Usage Count": 2},
            {"Payment Method": "Cash on Delivery", "Usage Count": 3}
        ]
    },
    {
        "Name": "Priya",
        "Age": 28,
        "Gender": "Female",
        "Location": "Mumbai, Maharashtra",
        "Account Age": "5 years",
        "Visit Frequency": "7 visits in the last 10 days",
        "Purchase Frequency": "3 purchases in the last month",
        "Average Purchase Value": "Rs 5000 per purchase",
        "Cart Abandonment Rate": "1 abandoned cart in the last month",
        "Engagement with Promotions": "Clicked on 2 promotional emails in the last month",
        "Wishlist Activity": "Added 3 items to wishlist in the last month",
        "Browsing History": ["Fashion", "Cosmetics", "Home Decor"],
        "Subscription Status": "Yes",
        "Preferred Payment Methods": ["Credit Card", "Cash On Delivery", "Net Banking"],
        "user_id": "priya@hotmail.com",
        "Previous Orders": [
            {"Item Name": "Dress", "Cost": "Rs 7000", "Payment Method": "Credit Card", "Additional Cost": "Rs 50", "Cashback": "Rs 300"},
            {"Item Name": "Makeup Kit", "Cost": "Rs 3000", "Payment Method": "PayPal", "Additional Cost": "Rs 0", "Cashback": "Rs 200"},
            {"Item Name": "Shoes", "Cost": "Rs 4000", "Payment Method": "Net Banking", "Additional Cost": "Rs 0", "Cashback": "Rs 100"}
        ],
        "payment_usage": [
            {"Payment Method": "Amazon Pay UPI", "Usage Count": 3},
            {"Payment Method": "Google Pay", "Usage Count": 1},
            {"Payment Method": "PhonePe", "Usage Count": 2},
            {"Payment Method": "Credit Card", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Debit Card", "Usage Count": 3},
            {"Payment Method": "EMI", "Usage Count": 0},
            {"Payment Method": "Net Banking", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Cash on Delivery", "Usage Count": random.randint(0, 30)}
        ]
    },
    {
        "Name": "Amit",
        "Age": 35,
        "Gender": "Male",
        "Location": "Delhi, Delhi",
        "Account Age": "7 years",
        "Visit Frequency": "3 visits in the last 10 days",
        "Purchase Frequency": "2 purchases in the last month",
        "Average Purchase Value": "Rs 10000 per purchase",
        "Cart Abandonment Rate": "2 abandoned carts in the last month",
        "Engagement with Promotions": "Clicked on 1 promotional email in the last month",
        "Wishlist Activity": "Added 2 items to wishlist in the last month",
        "Browsing History": ["Electronics", "Fitness Equipment", "Gardening Tools"],
        "Subscription Status": "No",
        "Preferred Payment Methods": ["Debit Card", "UPI", "Amazon Pay", "Cash On Delivery"],
        "user_id": "amit123@gmail.com",
        "Previous Orders": [
            {"Item Name": "Smart TV", "Cost": "Rs 60000", "Payment Method": "Debit Card", "Additional Cost": "Rs 500", "Cashback": "Rs 1000"},
            {"Item Name": "Bluetooth Speakers", "Cost": "Rs 8000", "Payment Method": "UPI", "Additional Cost": "Rs 50", "Cashback": "Rs 300"}
        ],
        "payment_usage": [
            {"Payment Method": "Amazon Pay UPI", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Google Pay", "Usage Count": 1},
            {"Payment Method": "PhonePe", "Usage Count": 2},
            {"Payment Method": "Credit Card", "Usage Count": 0},
            {"Payment Method": "Debit Card", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "EMI", "Usage Count": 0},
            {"Payment Method": "Net Banking", "Usage Count": 2},
            {"Payment Method": "Cash on Delivery", "Usage Count": random.randint(0, 30)}
        ]
    },
    {
        "Name": "Ananya",
        "Age": 24,
        "Gender": "Female",
        "Location": "Bangalore, Karnataka",
        "Account Age": "2 years",
        "Visit Frequency": "6 visits in the last 10 days",
        "Purchase Frequency": "5 purchases in the last month",
        "Average Purchase Value": "Rs 4000 per purchase",
        "Cart Abandonment Rate": "0 abandoned carts in the last month",
        "Engagement with Promotions": "Clicked on 4 promotional emails in the last month",
        "Wishlist Activity": "Added 6 items to wishlist in the last month",
        "Browsing History": ["Shoes", "Sports Equipment", "Travel Accessories"],
        "Subscription Status": "Yes",
        "Preferred Payment Methods": ["Debit Card", "Amazon Pay", "UPI", "Cash On Delivery"],
        "user_id": "ananya@gmail.com",
        "Previous Orders": [
            {"Item Name": "Running Shoes", "Cost": "Rs 5000", "Payment Method": "Amazon Pay", "Additional Cost": "Rs 100", "Cashback": "Rs 200"},
            {"Item Name": "Backpack", "Cost": "Rs 3000", "Payment Method": "Credit Card", "Additional Cost": "Rs 0", "Cashback": "Rs 150"},
            {"Item Name": "Fitness Band", "Cost": "Rs 4000", "Payment Method": "UPI", "Additional Cost": "Rs 50", "Cashback": "Rs 100"},
            {"Item Name": "Sunglasses", "Cost": "Rs 2000", "Payment Method": "Credit Card", "Additional Cost": "Rs 0", "Cashback": "Rs 50"},
            {"Item Name": "Travel Backpack", "Cost": "Rs 6000", "Payment Method": "Amazon Pay", "Additional Cost": "Rs 100", "Cashback": "Rs 300"}
        ],
        "payment_usage": [
            {"Payment Method": "Amazon Pay UPI", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Google Pay", "Usage Count": 3},
            {"Payment Method": "PhonePe", "Usage Count": 2},
            {"Payment Method": "Credit Card", "Usage Count": 2},
            {"Payment Method": "Debit Card", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "EMI", "Usage Count": 0},
            {"Payment Method": "Net Banking", "Usage Count": 2},
            {"Payment Method": "Cash on Delivery", "Usage Count": random.randint(0, 30)}
        ]
    },
    {
        "Name": "Suresh",
        "Age": 30,
        "Gender": "Male",
        "Location": "Chennai, Tamil Nadu",
        "Account Age": "4 years",
        "Visit Frequency": "4 visits in the last 10 days",
        "Purchase Frequency": "3 purchases in the last month",
        "Average Purchase Value": "Rs 8000 per purchase",
        "Cart Abandonment Rate": "1 abandoned cart in the last month",
        "Engagement with Promotions": "Clicked on 2 promotional emails in the last month",
        "Wishlist Activity": "Added 4 items to wishlist in the last month",
        "Browsing History": ["Home Appliances", "Gaming Consoles", "Cookware"],
        "Subscription Status": "No",
        "Preferred Payment Methods": ["Debit Card", "UPI", "Net Banking"],
        "user_id": "suresh@gmail.com",
        "Previous Orders": [
            {"Item Name": "Refrigerator", "Cost": "Rs 25000", "Payment Method": "Net Banking", "Additional Cost": "Rs 200", "Cashback": "Rs 500"},
            {"Item Name": "Air Conditioner", "Cost": "Rs 35000", "Payment Method": "Debit Card", "Additional Cost": "Rs 300", "Cashback": "Rs 1000"},
            {"Item Name": "Microwave Oven", "Cost": "Rs 12000", "Payment Method": "UPI", "Additional Cost": "Rs 0", "Cashback": "Rs 300"}
        ],
        "payment_usage": [
            {"Payment Method": "Amazon Pay UPI", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Google Pay", "Usage Count": 3},
            {"Payment Method": "PhonePe", "Usage Count": 2},
            {"Payment Method": "Credit Card", "Usage Count": 0},
            {"Payment Method": "Debit Card", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "EMI", "Usage Count": 0},
            {"Payment Method": "Net Banking", "Usage Count": random.randint(0,30)},
            {"Payment Method": "Cash on Delivery", "Usage Count": 2}
        ]
    },
    {
        "Name": "Akanksha",
        "Age": 25,
        "Gender": "Female",
        "Location": "Pune, Maharashtra",
        "Account Age": "4 years",
        "Visit Frequency": "3 visits in the last 10 days",
        "Purchase Frequency": "2 purchases in the last month",
        "Average Purchase Value": "Rs 6000 per purchase",
        "Cart Abandonment Rate": "2 abandoned carts in the last month",
        "Engagement with Promotions": "Clicked on 1 promotional email in the last month",
        "Wishlist Activity": "Added 3 items to wishlist in the last month",
        "Browsing History": ["Home Decor", "Fashion Accessories", "Outdoor Gear"],
        "Subscription Status": "No",
        "Preferred Payment Methods": ["Amazon Pay", "UPI"],
        "user_id": "akanksha@gmail.com",
        "Previous Orders": [
            {"Item Name": "Wall Art", "Cost": "Rs 4000", "Payment Method": "Credit Card", "Additional Cost": "Rs 50", "Cashback": "Rs 100"},
            {"Item Name": "Necklace", "Cost": "Rs 6000", "Payment Method": "UPI", "Additional Cost": "Rs 0", "Cashback": "Rs 150"}
        ],
        "payment_usage": [
            {"Payment Method": "Amazon Pay UPI", "Usage Count": random.randint(0, 30)},
            {"Payment Method": "Google Pay", "Usage Count": 1},
            {"Payment Method": "PhonePe", "Usage Count": 2},
            {"Payment Method": "Credit Card", "Usage Count": 2},
            {"Payment Method": "Debit Card", "Usage Count": 5},
            {"Payment Method": "EMI", "Usage Count": 0},
            {"Payment Method": "Net Banking", "Usage Count": 2},
            {"Payment Method": "Cash on Delivery", "Usage Count": 3}
        ]
    }
]

# Add unique transaction ID to each previous order
for user in users:
    for order in user["Previous Orders"]:
        order["Transaction ID"] = str(uuid.uuid4())

# Function to connect to MongoDB and insert data
def insert_data(data):
    try:
        client = MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
        db = client["amazon"]
        collection = db["user_profiles"]
        collection.insert_many(data)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

# Insert the user profile data
insert_data(users)
