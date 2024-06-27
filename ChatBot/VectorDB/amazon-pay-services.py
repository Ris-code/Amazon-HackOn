import sys
import os
from langchain_mistralai import ChatMistralAI
from langchain.schema import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
# os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY_ACCOUNT_2")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

def document_split(services):
    # Initialize an empty list to store Document objects
    documents = []

    # Convert FAQs to Document objects
    for service in services:
        content = f"Service: {service}\nDescription: {services[service]}"
        metadata = {
            "Service": service
        }
        documents.append(Document(page_content=content, metadata=metadata))

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Split documents into chunks
    all_splits = text_splitter.split_documents(documents)

    return all_splits

def pinecone_vector_store(services):
    index_name = "amazon-services"  
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    else:
        print("The index already exist so enter a new index name")

    index = pc.Index(index_name)

    docs = document_split(services)

    PineconeVectorStore.from_documents(docs, embedding=MistralAIEmbeddings(), index_name=index_name)

amazon_services = {"Smart Stores" : """Amazon Pay launches Smart Stores

    A smart and contactless way for customers to discover products at local shops, make payments, get EMIs and earn rewards using Amazon Pay.
    Amazon Pay today announced the launch of “Smart Stores”; customers simply scan the store’s QR code using the Amazon app to begin exploring the products available within the store. After selecting the products, they wish to buy they checkout with Amazon Pay, which gives them a choice of using UPI, balance, or credit or debit cards. Customers can on-the-spot convert a transaction into an EMI, and from time-to-time avail exciting rewards from their banks or through Amazon Pay. What’s more - the bill is delivered digitally, making the entire journey contactless, convenient and rewarding.

    Amazon Pay’s Smart Store empowers local shops with the following capabilities to increase footfalls, improve customer experience and generate more sales.

    · Digital Storefront: Enables a local shop to launch a digital storefront thereby enabling its customers to discover products, read reviews, evaluate offers while in the store or from anywhere using the Amazon app.

    · Contactless Payments with EMIs and Bank Offers: Enables merchants to offer the entire suite of contactless payment options including UPI, balance, credit and debit cards, EMIs and bank offers, and send a digital bill to reduce contact and save costs.

    · Amazon Pay Rewards: Enables local shops to offer Amazon Pay reward coupons to attract new customers, as well as incentivize customers to come back to them for their next purchase, thus increasing footfalls.

    “Amazon Pay is already accepted at millions of local shops, we are trying to make customers’ buying experience at local shops even more convenient and safe through Smart Stores. Further, through EMIs, bank offers and rewards, we seek to make these purchases more affordable and rewarding for customers, and help increase sales for merchants.” said Mahendra Nerurkar, CEO, Amazon Pay.

    Thousands of local shops across the country have already signed up as Amazon Pay Smart Stores. These include local shops like Sri Balaji Kitchens-Vishakapatnam, USHA Company Store-Jabalpur and outlets of brands such as Big Bazaar, MedPlus and More Supermarkets. Amazon Pay has partnered with leading banks to offer customers the best value and in-store purchasing experience.

    Learn more about Amazon Pay Smart Stores (https://www.amazon.in/b?language=en_IN&node=20959800031).""",

"Car and Bike Insurance": """Amazon Pay launches car and bike insurance with easy online purchase

    Auto insurance Amazon India
    Partners with Acko to offer insurance at low prices. Exclusive benefits for Prime members
    Amazon Pay marked its foray in the insurance space by offering two and four-wheeler insurance policies, in partnership with Acko General Insurance Ltd. Customers can now purchase insurance in less than two minutes with no paperwork. Prime members get extra benefits including additional discounts.

    The experience of buying insurance has been made easy by Amazon Pay in partnership with Acko, by providing simple and easy to understand purchase journey that facilitates customers to buy insurance effortlessly in a few easy steps. This coupled with services like hassle-free claims with zero paperwork, one-hour pick-up, 3-day assured claim servicing and 1 year repair warranty - in select cities, as well as an option for instant cash settlements for low value claims, making it beneficial for customers.

    Customers can buy Auto Insurance from the Amazon Pay page or just search for it. They can get a quote for their car or bike’s insurance in a few simple steps by providing basic details. Additionally, they can select from a list of add-ons like zero-depreciation, engine protection, and more. Customers can pay using Amazon Pay balance, UPI, or any saved card and the policy will be in their email inbox in less than 2-minutes. A copy of the policy can also be downloaded from Your Orders page.

    Commenting on the launch Vikas Bansal, Director & Head of Financial Services Amazon Pay India said “Our vision is to make Amazon Pay the most, trusted, convenient and rewarding way to pay for our customers. Delighted by this experience, there has been a growing demand for more services. In line with this need, we are excited to launch an auto insurance product that is affordable, convenient, and provides a seamless claims experience”.

    Varun Dua, CEO, Acko General Insurance said “We are happy to partner with Amazon Pay to offer an auto insurance proposition that has been designed with the customer at the centre. Through this product we aim to deliver a superior consumer experience right from purchase to claims by making it more affordable, accessible and seamless. This launch also marks an important milestone in our successful partnership with Amazon and we are excited about the journey ahead.”

    Customers can now visit the Amazon Pay page or search on the Amazon mobile app or the mobile website to buy car and bike insurance in a few easy steps. Click here(https://www.amazon.in/ap/signin?openid.pape.max_auth_age=3600&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fauto-insurance&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_insurance_in&openid.mode=checkid_setup&language=en_US&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0) for more information on Auto Insurance.""",

"Book Train Tickets": """Now, book train tickets with Amazon Pay
    Amazon India partners with IRCTC; launches online reserved train ticket bookings with zero fees
    Amazon India has partnered with ‘Indian Railway Catering and Tourism Corporation’ (IRCTC), to provide their customers with the facility to book reserved train tickets on Amazon. Customers will get a 10% cashback of up to INR 100 on their first train ticket booking and Prime members can avail 12% cashback up to INR 120/- for these bookings. This offer is valid for a limited period of time. For the introductory period, Amazon.in has also waived off service and payment gateway transaction charges. With this launch, Amazon Pay adds another travel category, thereby offering its customers a one-stop-shop for booking flights, bus and train tickets.

    Amazon Pay Train Ticket Booking
    NOW BOOK TRAIN TICKETS
    We are excited to partner with IRCTC and move another step forward in making life easy and convenient for our customers.
    Vikas Bansal, Director - Amazon Pay
    With this new offering, customers will be able to check seat and quota availability across all train classes on the Amazon app. They can pre-load money into their Amazon Pay Balance wallet to make this experience even smoother and pay in a single click. Amazon.in presents its customers with a variety of self-serve options such as live checking of PNR status (for ticket booked on Amazon only), downloads and cancellations of tickets booked on Amazon. Customers paying with Amazon Pay Balance also get instant refund in case of cancellations or booking failures, giving them a hassle-free experience.

    Speaking on the launch, Vikas Bansal, Director - Amazon Pay said, “We are excited to partner with IRCTC and move another step forward in making life easy and convenient for our customers. Last year, we launched flights, and bus ticket booking on Amazon. With the facility to book reserved train tickets on our platform, we are enabling travel across any mode preferred by customers. Over the course of time, the Amazon app has become the one stop destination for shopping and payment of several other use cases. Customers love the convenience we offer of shopping and paying - all in one single app.”

    The feature is open to Android and iOS app users. Customers can book their tickets by clicking the trains/ travel category under the Amazon Pay tab. They can easily select their route/travel dates and get a list of all available trains. Customers can use their Amazon Pay balance or Amazon Pay ICICI credit card or any other digital payment methods for an easy checkout experience. In case customers need to cancel a ticket, they can do so under the ‘Your Orders’ section. They can also seek 24x7 help through an Amazon helpline over phone and chat.
""",

"Amazon Pay UPI": """Amazon Pay UPI launched for Android customers

    Link your bank account on Amazon Pay and use it to pay for everything – shopping, everyday needs, and bill payments
    In its continuous effort make payments more secure and convenient, Amazon announces the launch of Amazon Pay UPI for Android users. Amazon Pay has partnered with Axis Bank to issue UPI IDs to its customers. Customers can now link their bank account on their Amazon mobile app and make fast, easy, and secure payments directly from bank account. Customers can use their Amazon Pay UPI ID to shop on Amazon.in, and also to make payments for their everyday needs including recharges and bill payments without entering bank account or debit card credentials, or going through a multi-layer process to pay from their bank account.

    This association with Amazon is a step in offering consumers more options and seamless experiences while using UPI.
    Vishal Kanvaty, SVP Product & Innovations at National Payments Corporation of India (NPCI)
    With this launch, Amazon Pay customers will get a seamless experience for digital payments using their Bank account to make payments without having to enter CVV or OTP, remembering net-banking customer ID, bank account number or other such details. Every customer transaction on Amazon is secured through mobile device verification as well as the UPI PIN. Customers can link their bank account and complete one time set up process by setting up a UPI PIN, after which they can make instant payments. This launch is a key step to enable Amazon customers in adopting BHIM UPI as a digital payment method, thereby helping in the Govt. of India’s Cashless India initiative.

    Vishal Kanvaty, SVP Product & Innovations at National Payments Corporation of India (NPCI), said “Our goal is to ensure simple, secure and seamless consumer experience while making payments. This association with Amazon is a step in offering consumers more options and seamless experiences while using UPI. We are excited that millions of customers on Amazon will now be able to make digital payments through UPI to buy products from Amazon’s entire seller base.”

    “We are very excited with our Amazon Pay UPI launch, this will offer a fast, seamless and secure digital payment experience on Amazon.in. Through Amazon Pay UPI, we are enabling customers paying through cash and bank accounts to make digital one-step payments for their shopping and other payment needs. We are constantly working towards delivering an awesome experience for our customers and the launch of Amazon Pay UPI is a key milestone in this journey. This launch will help accelerate adoption of merchant payments on UPI platform.” said Vikas Bansal, Director - Amazon Pay

    Commenting on the partnership, Sanjeev Moghe, Head Cards & Payments, Axis Bank said “Axis Bank has always been at the forefront of promoting a digitized economy and has been making sustained investments in new cashless and digital payment methods. We are excited to partner with Amazon to implement the UPI ID for its customers. This partnership will help millions of customers enjoy safe and seamless online payments through the UPI mode of payment.”

    Amazon Pay will continue to leverage UPI platform to launch new features to further simplify customer experience and expand into new use cases. Amazon is committed to the long-term vision of a less-cash India and continues to invest in experiences, which reduce customer friction, improve affordability and foster everyday habits, thereby building preference for digital payment. To try out the Amazon Pay UPI payments experience, log into Amazon from your Android mobile phone and choose UPI as your payment method to shop on Amazon.
""",

"Amazon Pay Later": """Amazon Pay launches Amazon Pay Later

    Amazon Pay Launches Amazon Pay Later in India
    Amazon will offer an instant credit line to customers to purchase essentials, electronics, fashion, groceries and pay their monthly utility bills
    Amazon Pay today launched ‘Amazon Pay Later’, a service that will extend a virtual line of credit to eligible customers shopping on Amazon.in. With an easy digital sign-up process, customers will get access to instant credit that they can use to buy any product ranging from daily essentials to electronics and clothing items. Customers can also use this credit to complete their bill payments on Amazon.in. Amazon Pay Later service offers the option to repay in the subsequent month at no additional fees, or in easy EMIs up to 12 months at nominal interest rates.

    Amazon Pay Later is a unique service that will help customers expand their access to credit and experience most convenient option of making payments.
    Mahendra Nerurkar, CEO, Amazon Pay India
    This initiative by Amazon Pay is aimed at helping customers extend their budgets for purchases like home appliances, electronic gadgets, everyday essentials, groceries, and even pay their monthly bills be it electricity, mobile recharges, DTH etc. As a pilot, this unique service was available to a small set of customers and Amazon Pay has now extended this service to lakhs of eligible customers. Amazon Pay has partnered with Capital Float and The Karur Vysya Bank(KVB) to design and enable ‘Amazon Pay Later’ service for its eligible customers.

    ‘Amazon Pay Later’ offers a seamless payment experience with in-built security features and gives customers and option to setup auto-repayment to settle monthly bill or EMIs through the bank of their choice. Customers also have an option to repay all outstanding amount in one go at no additional fees. Based on usage and repayment behavior customers will also be able to enhance their credit limit further.

    “We are always looking for ways to improve our customers’ payments experience on Amazon.in and make purchases more affordable. Amazon Pay Later is a unique service that will help customers expand their access to credit and experience most convenient option of making payments. In current times Amazon Pay later empowers our customers to better manage their monthly spends,” said Mahendra Nerurkar, CEO Amazon Pay India.

    Why choose Amazon Pay Later?
    Customer can share their PAN card number and Aadhar card number and register in 3 simple steps
    You can pay next month at 0% interest or pay in 3 to 12 month EMIs. There are no hidden charges
    You don't need a credit card
    You can avail of credit upto INR 20,000
    You can set up an automatic repayment schedule
    Know more about how to register and key benefits by clicking here(https://www.amazon.in/b?node=15430915031)
""",

"Small & medium businesses use Amazon Pay": """50 lakh small & medium businesses now use Amazon Pay

    Kirana stores, service providers, small eateries & more enabled to accept digital payments through Amazon Pay’s QR Code. Amazon Pay For Business app launched for small & medium businesses to enable seamless acceptance of digital payments.
    As part of Amazon’s commitment to digitally enable small & medium businesses (SMBs) in India, Amazon Pay today announced that it has empowered over 50 lakh neighborhood stores & businesses with its digital payments infrastructure. These SMBs, most of whom earlier transacted only in cash, can now accept payments from their customers using Amazon Pay’s QR Code.

    This milestone achievement was revealed by Amazon’s Senior Vice President, Russell Grandinetti, in conversation with Nandan Nilekani during the session ‘innovating for a better India’ at Amazon Smbhav.

    Amazon Pay has also launched the “Amazon Pay For Business” mobile app to simplify accepting digital payments for SMBs. Currently available on Android, the app can be used by businesses across the country to register themselves, generate a unique QR code and start accepting digital payments within minutes. Customers can use any UPI app to scan the Amazon QR code and make a payment to these businesses.

    Mahendra Nerurkar, CEO, Amazon Pay India who moderated this session said “Small & medium businesses are the backbone of our nation’s economy. By enabling more than 50 lakh small business owners and entreprenuers to accept digital payments, we are expediting their inclusion into digital India. The Amazon Pay For Business app will further catalyse this adoption and enable merchants to enter the digital payments ecosystem in minutes. We have built and scaled our digital payment acceptance for SMBs using UPI that is inarguably one of the world’s biggest digital payments platform and look forward to creating more products that transform the way India pays.”

    Over 50 lakh small & medium businesses who use Amazon Pay constitute a diverse set of merchants and entrepreneurs. More than 25 lakh operate retail & shopping outlets such as kirana stores, about 10 lakh operate food & beverage outlets such as restaurants & small eateries, over 5 lakh offer services such as salons, close to 4 lakh offer health & medical care while the remaining comprise of vocations such as taxi drivers, auto drivers, plumbers and more.

    To start using Amazon Pay, merchants can download the Amazon Pay For Business mobile app on the Google Playstore by clicking here(https://play.google.com/store/apps/details?id=com.amazon.in.payments.merchant.app.android&hl=None&pli=1).
"""
}

pinecone_vector_store(amazon_services)