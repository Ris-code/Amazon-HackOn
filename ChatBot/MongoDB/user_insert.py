from pymongo import MongoClient
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Define the user profile schema as a Python dictionary
l = [
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
  "Browsing History": [
    "Laptops",
    "Smartphones",
    "Books"
  ],
  "Subscription Status": "No",
  "Preferred Payment Methods": [
    "Credit Card",
    "Mobile Wallet",
    "Amazon Pay",
    "UPI",
    "Debit Card"
  ],
  "user_id": "rishav@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Laptop",
      "Cost": "Rs 50,000",
      "Payment Method": "Credit Card",
      "Additional Cost": "Rs 2",
      "Cashback": "Rs 400"
    },
    {
      "Item Name": "Smartphone",
      "Cost": "Rs 20,000",
      "Payment Method": "Amazon Pay",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 1000"
    },
    {
      "Item Name": "Headphones",
      "Cost": "Rs 5000",
      "Payment Method": "Debit Card",
      "Additional Cost": "Rs 100",
      "Cashback": "Rs 200"
    },
    {
      "Item Name": "Fitness Tracker",
      "Cost": "Rs 3000",
      "Payment Method": "UPI",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 150"
    }
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
  "Browsing History": [
    "Fashion",
    "Cosmetics",
    "Home Decor"
  ],
  "Subscription Status": "Yes",
  "Preferred Payment Methods": [
    "Credit Card",
    "PayPal",
    "Net Banking"
  ],
  "user_id": "priya@hotmail.com",
  "Previous Orders": [
    {
      "Item Name": "Dress",
      "Cost": "Rs 7000",
      "Payment Method": "Credit Card",
      "Additional Cost": "Rs 50",
      "Cashback": "Rs 300"
    },
    {
      "Item Name": "Makeup Kit",
      "Cost": "Rs 3000",
      "Payment Method": "PayPal",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 200"
    },
    {
      "Item Name": "Shoes",
      "Cost": "Rs 4000",
      "Payment Method": "Net Banking",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 100"
    }
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
  "Browsing History": [
    "Electronics",
    "Fitness Equipment",
    "Gardening Tools"
  ],
  "Subscription Status": "No",
  "Preferred Payment Methods": [
    "Debit Card",
    "UPI"
  ],
  "user_id": "amit123@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Smart TV",
      "Cost": "Rs 60000",
      "Payment Method": "Debit Card",
      "Additional Cost": "Rs 500",
      "Cashback": "Rs 1000"
    },
    {
      "Item Name": "Bluetooth Speakers",
      "Cost": "Rs 8000",
      "Payment Method": "UPI",
      "Additional Cost": "Rs 50",
      "Cashback": "Rs 300"
    }
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
  "Browsing History": [
    "Shoes",
    "Sports Equipment",
    "Travel Accessories"
  ],
  "Subscription Status": "Yes",
  "Preferred Payment Methods": [
    "Credit Card",
    "Amazon Pay",
    "UPI"
  ],
  "user_id": "ananya@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Running Shoes",
      "Cost": "Rs 5000",
      "Payment Method": "Amazon Pay",
      "Additional Cost": "Rs 100",
      "Cashback": "Rs 200"
    },
    {
      "Item Name": "Backpack",
      "Cost": "Rs 3000",
      "Payment Method": "Credit Card",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 150"
    },
    {
      "Item Name": "Fitness Band",
      "Cost": "Rs 4000",
      "Payment Method": "UPI",
      "Additional Cost": "Rs 50",
      "Cashback": "Rs 100"
    },
    {
      "Item Name": "Sunglasses",
      "Cost": "Rs 2000",
      "Payment Method": "Credit Card",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 50"
    },
    {
      "Item Name": "Travel Backpack",
      "Cost": "Rs 6000",
      "Payment Method": "Amazon Pay",
      "Additional Cost": "Rs 100",
      "Cashback": "Rs 300"
    }
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
  "Browsing History": [
    "Home Appliances",
    "Gaming Consoles",
    "Cookware"
  ],
  "Subscription Status": "No",
  "Preferred Payment Methods": [
    "Debit Card",
    "UPI",
    "Net Banking"
  ],
  "user_id": "suresh@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Refrigerator",
      "Cost": "Rs 25000",
      "Payment Method": "Net Banking",
      "Additional Cost": "Rs 200",
      "Cashback": "Rs 500"
    },
    {
      "Item Name": "Air Conditioner",
      "Cost": "Rs 35000",
      "Payment Method": "Debit Card",
      "Additional Cost": "Rs 300",
      "Cashback": "Rs 1000"
    },
    {
      "Item Name": "Microwave Oven",
      "Cost": "Rs 12000",
      "Payment Method": "UPI",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 300"
    }
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
  "Browsing History": [
    "Home Decor",
    "Fashion Accessories",
    "Outdoor Gear"
  ],
  "Subscription Status": "No",
  "Preferred Payment Methods": [
    "Credit Card",
    "PayPal",
    "UPI"
  ],
  "user_id": "akanksha@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Sofa Set",
      "Cost": "Rs 25000",
      "Payment Method": "Credit Card",
      "Additional Cost": "Rs 200",
      "Cashback": "Rs 500"
    },
    {
      "Item Name": "Handbag",
      "Cost": "Rs 5000",
      "Payment Method": "UPI",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 100"
    }
  ]
},

{
  "Name": "Vikram",
  "Age": 32,
  "Gender": "Male",
  "Location": "Hyderabad, Telangana",
  "Account Age": "6 years",
  "Visit Frequency": "4 visits in the last 10 days",
  "Purchase Frequency": "3 purchases in the last month",
  "Average Purchase Value": "Rs 7000 per purchase",
  "Cart Abandonment Rate": "1 abandoned cart in the last month",
  "Engagement with Promotions": "Clicked on 2 promotional emails in the last month",
  "Wishlist Activity": "Added 4 items to wishlist in the last month",
  "Browsing History": [
    "Gadgets",
    "Home Appliances",
    "Fitness Gear"
  ],
  "Subscription Status": "Yes",
  "Preferred Payment Methods": [
    "Debit Card",
    "Amazon Pay",
    "Net Banking"
  ],
  "user_id": "vikram123@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Smartwatch",
      "Cost": "Rs 12000",
      "Payment Method": "Debit Card",
      "Additional Cost": "Rs 100",
      "Cashback": "Rs 300"
    },
    {
      "Item Name": "Water Purifier",
      "Cost": "Rs 15000",
      "Payment Method": "Amazon Pay",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 500"
    },
    {
      "Item Name": "Wireless Earphones",
      "Cost": "Rs 8000",
      "Payment Method": "Net Banking",
      "Additional Cost": "Rs 50",
      "Cashback": "Rs 200"
    }
  ]
},

{
  "Name": "Aarav",
  "Age": 40,
  "Gender": "Male",
  "Location": "Jaipur, Rajasthan",
  "Account Age": "8 years",
  "Visit Frequency": "2 visits in the last 10 days",
  "Purchase Frequency": "1 purchase in the last month",
  "Average Purchase Value": "Rs 25000",
  "Cart Abandonment Rate": "0 abandoned carts in the last month",
  "Engagement with Promotions": "Clicked on 1 promotional email in the last month",
  "Wishlist Activity": "Added 1 item to wishlist in the last month",
  "Browsing History": [
    "Art and Craft Supplies",
    "Antiques",
    "Collectibles"
  ],
  "Subscription Status": "No",
  "Preferred Payment Methods": [
    "Credit Card",
    "UPI"
  ],
  "user_id": "aarav@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Painting",
      "Cost": "Rs 30000",
      "Payment Method": "Credit Card",
      "Additional Cost": "Rs 100",
      "Cashback": "Rs 200"
    }
  ]
},

{
  "Name": "Shreya",
  "Age": 22,
  "Gender": "Female",
  "Location": "Kolkata, West Bengal",
  "Account Age": "3 years",
  "Visit Frequency": "6 visits in the last 10 days",
  "Purchase Frequency": "4 purchases in the last month",
  "Average Purchase Value": "Rs 3500 per purchase",
  "Cart Abandonment Rate": "1 abandoned cart in the last month",
  "Engagement with Promotions": "Clicked on 3 promotional emails in the last month",
  "Wishlist Activity": "Added 5 items to wishlist in the last month",
  "Browsing History": [
    "Fashion",
    "Books",
    "Beauty Products"
  ],
  "Subscription Status": "Yes",
  "Preferred Payment Methods": [
    "Debit Card",
    "PayPal",
    "UPI"
  ],
  "user_id": "shreya@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Dress",
      "Cost": "Rs 4000",
      "Payment Method": "Debit Card",
      "Additional Cost": "Rs 50",
      "Cashback": "Rs 100"
    },
    {
      "Item Name": "Cosmetics Kit",
      "Cost": "Rs 3000",
      "Payment Method": "UPI",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 50"
    },
    {
      "Item Name": "Novel Set",
      "Cost": "Rs 2500",
      "Payment Method": "PayPal",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 50"
    },
    {
      "Item Name": "Perfume",
      "Cost": "Rs 3500",
      "Payment Method": "Debit Card",
      "Additional Cost": "Rs 0",
      "Cashback": "Rs 150"
    }
  ]
},

{
  "Name": "Kartik",
  "Age": 27,
  "Gender": "Male",
  "Location": "Chandigarh, Punjab",
  "Account Age": "5 years",
  "Visit Frequency": "5 visits in the last 10 days",
  "Purchase Frequency": "2 purchases in the last month",
  "Average Purchase Value": "Rs 9000 per purchase",
  "Cart Abandonment Rate": "2 abandoned carts in the last month",
  "Engagement with Promotions": "Clicked on 2 promotional emails in the last month",
  "Wishlist Activity": "Added 4 items to wishlist in the last month",
  "Browsing History": [
    "Electronics",
    "Gaming Consoles",
    "Home Appliances"
  ],
  "Subscription Status": "No",
  "Preferred Payment Methods": [
    "Credit Card",
    "Amazon Pay",
    "Net Banking"
  ],
  "user_id": "kartik@gmail.com",
  "Previous Orders": [
    {
      "Item Name": "Gaming Laptop",
      "Cost": "Rs 80000",
      "Payment Method": "Credit Card",
      "Additional Cost": "Rs 500",
      "Cashback": "Rs 1000"
    },
    {
      "Item Name": "Smartphone",
      "Cost": "Rs 35000",
      "Payment Method": "Amazon Pay",
      "Additional Cost": "Rs 200",
      "Cashback": "Rs 800"
    }
  ]
},
]
# Function to add a user profile to MongoDB
def add_user_profile(user_profile):
    # MongoDB connection details
    client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))  
    db = client['amazon']  
    collection = db['user_profiles']  
    
    # Insert the user profile into the MongoDB collection
    collection.insert_one(user_profile)
    print("User profile added successfully!")
    # print(user_profile)

for user_profile in l:
    add_user_profile(user_profile)
