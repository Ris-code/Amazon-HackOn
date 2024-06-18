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
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# Define a function to split documents into chunks
def document_split(questions, category):
    documents = []

    # content = f"Category: {category}\n"
    # question_meta = ""
    for qna_pair in questions:
        question = qna_pair["question"]
        answer = qna_pair["answer"]
        content = f"Category: {category}\nQuestion: {question}\nAnswer:\n{answer}"
        metadata = {"category": category, "question": question}
        documents.append(Document(page_content=content, metadata=metadata))

    
    # metadata = {"category": category, "question": question_meta}
        # category_questions.append(Document(page_content=content, metadata=metadata))
    # documents.append(Document(page_content=content, metadata=metadata))

        # documents.append(category_questions)
    print(documents)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    all_splits = text_splitter.split_documents(documents)

    return all_splits
    
def pinecone_vector_store(data, category):
    index_name = "query-category-new"
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
        print(f"The index '{index_name}' already exists.")

    index = pc.Index(index_name)
    docs = document_split(data, category)
    
    PineconeVectorStore.from_documents(docs, embedding=MistralAIEmbeddings(), index_name=index_name)

query_category = {
    "Payment Failure": [
        {
            "question": "Why did my payment fail?",
            "answer": "Your payment may have failed for several reasons. Common causes include incorrect card details, such as an incorrect card number, expiration date, or CVV. Additionally, your bank may have declined the transaction due to insufficient funds, an expired card, or a security block. Network issues or temporary problems with the payment gateway can also result in payment failures. To resolve this, please verify your card information, ensure that you have sufficient funds, and try again. If the issue persists, consider using an alternative payment method or contacting your bank for further assistance."
        },
        {
            "question": "Can you help me with a payment failure issue?",
            "answer": "Certainly! Here are some steps to troubleshoot payment failures on Amazon:\n1. Double-check your card details, including the card number, expiration date, and CVV.\n2. Ensure that there are sufficient funds in your account to cover the purchase.\n3. Check if your card has expired or if there are any restrictions placed by your bank.\n4. Try using a different payment method, such as another credit card, debit card, or Amazon Pay balance.\n5. Contact your bank to inquire about any potential issues with your account or card.\nIf you continue to experience difficulties, please reach out to Amazon Customer Service for personalized assistance."
        },
        {
            "question": "What are the common reasons for payment failure?",
            "answer": "Common reasons for payment failure on Amazon include:\n1. Incorrect card details: Ensure the card number, expiration date, and CVV are entered correctly.\n2. Insufficient funds: Verify that your account has enough funds to complete the transaction.\n3. Expired card: Check if your card has expired and, if so, use a different card.\n4. Bank restrictions: Your bank may decline the transaction for security reasons or due to restrictions on your account. Contact your bank for more information.\n5. Network issues: Temporary network problems can cause payment failures. Wait a few moments and try again.\n6. Payment gateway issues: Sometimes, issues with the payment gateway can result in failures. If this happens, try a different payment method.\nIf none of these apply, please contact Amazon Customer Service for further assistance."
        },
        {
            "question": "How can I retry a failed payment?",
            "answer": "To retry a failed payment on Amazon, follow these steps:\n1. Log in to your Amazon account and go to 'Your Orders'.\n2. Find the order with the failed payment and click on 'Retry Payment'.\n3. Review and update your payment information if necessary, then click 'Confirm' to retry the payment.\n4. Ensure that your card details are correct, and that there are sufficient funds in your account.\nIf the payment still fails, consider using an alternative payment method or contacting your bank for more assistance."
        },
        {
            "question": "What should I do if my payment keeps failing?",
            "answer": "If your payment keeps failing, try the following steps:\n1. Verify your card details: Ensure the card number, expiration date, and CVV are entered correctly.\n2. Check your account balance: Make sure you have sufficient funds to complete the purchase.\n3. Use a different payment method: Try another credit card, debit card, or Amazon Pay balance.\n4. Contact your bank: There might be a restriction or security block on your card. Contact your bank to resolve any issues.\n5. Clear your browser cache: Sometimes, clearing your browser cache can resolve technical issues.\n6. Use a different device or browser: Try completing the transaction on a different device or using a different browser.\nIf none of these solutions work, please reach out to Amazon Customer Service for further assistance."
        },
        {
            "question": "Is there a way to ensure my payment goes through successfully?",
            "answer": "To ensure your payment goes through successfully on Amazon, consider the following tips:\n1. Double-check your card details: Ensure the card number, expiration date, and CVV are entered correctly.\n2. Verify your account balance: Make sure you have enough funds in your account to cover the purchase.\n3. Ensure your card is active and not expired: Contact your bank if you're unsure about the status of your card.\n4. Use a reliable internet connection: A stable internet connection helps prevent interruptions during the payment process.\n5. Try using a different payment method: Use another credit card, debit card, or Amazon Pay balance if you encounter issues.\n6. Contact your bank: Inform your bank about the transaction to ensure it isn't blocked for security reasons.\n7. Clear your browser cache: This can help resolve any technical issues related to your browser.\nIf you continue to experience difficulties, please reach out to Amazon Customer Service for further assistance."
        },
        {
            "question": "Why is my credit card being declined?",
            "answer": "Your credit card may be declined for several reasons, including:\n1. Incorrect card details: Ensure the card number, expiration date, and CVV are entered correctly.\n2. Insufficient funds: Verify that your account has enough funds to complete the transaction.\n3. Expired card: Check if your card has expired and, if so, use a different card.\n4. Bank restrictions: Your bank may decline the transaction for security reasons or due to restrictions on your account. Contact your bank for more information.\n5. Daily spending limit: Some cards have daily spending limits which may have been reached.\n6. Suspected fraudulent activity: If your bank suspects fraudulent activity, they may decline the transaction. Contact your bank to resolve this issue.\nIf none of these apply, please contact Amazon Customer Service for further assistance."
        },
        {
            "question": "How can I resolve a payment processing error?",
            "answer": "To resolve a payment processing error on Amazon, follow these steps:\n1. Verify your card details: Ensure the card number, expiration date, and CVV are entered correctly.\n2. Check your account balance: Make sure you have sufficient funds to complete the purchase.\n3. Try a different payment method: Use another credit card, debit card, or Amazon Pay balance.\n4. Contact your bank: There might be a restriction or security block on your card. Contact your bank to resolve any issues.\n5. Clear your browser cache: Sometimes, clearing your browser cache can resolve technical issues.\n6. Use a different device or browser: Try completing the transaction on a different device or using a different browser.\nIf none of these solutions work, please reach out to Amazon Customer Service for further assistance."
        }
    ],

    "Order Confirmation": [
        {
            "question": "When will I receive my order confirmation?",
            "answer": "Typically, you should receive your order confirmation email within a few minutes after placing your order on Amazon. However, in some cases, it may take up to an hour due to high order volumes or technical issues. Please ensure you check your email's spam or junk folder, as the confirmation email might have been filtered there."
        },
        {
            "question": "Why haven't I received an order confirmation email yet?",
            "answer": "There are a few reasons why you might not have received your order confirmation email yet:\n1. Email delivery delays: Sometimes, high order volumes can cause delays in email delivery.\n2. Incorrect email address: Ensure that the email address associated with your Amazon account is correct.\n3. Spam/junk folder: Check your email's spam or junk folder as the confirmation email might have been filtered there.\n4. Technical issues: Occasionally, technical issues can delay the sending of confirmation emails. If you haven't received your confirmation email after an hour, please check your order history on Amazon to ensure your order was placed successfully."
        },
        {
            "question": "How long does it take to get an order confirmation?",
            "answer": "You should receive your order confirmation email within a few minutes of placing your order. However, during peak times or due to technical issues, it may take up to an hour. If you still haven't received your confirmation email after an hour, please check your order history in your Amazon account to confirm that your order was placed successfully. Also, check your email's spam or junk folder."
        },
        {
            "question": "Can I check the status of my order confirmation online?",
            "answer": "Yes, you can check the status of your order confirmation online. Log in to your Amazon account and go to 'Your Orders'. Here, you will see a list of your recent orders along with their current status. If your order has been successfully placed, it will be listed here even if you haven't received the confirmation email yet."
        },
        {
            "question": "What should I do if I don't get an order confirmation email?",
            "answer": "If you haven't received your order confirmation email, please follow these steps:\n1. Check your email's spam or junk folder to ensure the email wasn't filtered.\n2. Verify that the email address associated with your Amazon account is correct.\n3. Log in to your Amazon account and go to 'Your Orders' to check if your order was successfully placed.\n4. If your order is listed but you still haven't received the confirmation email, you can contact Amazon Customer Service for further assistance. They can resend the confirmation email or provide additional support."
        },
        {
            "question": "Is there a way to resend the order confirmation email?",
            "answer": "Yes, you can request Amazon to resend the order confirmation email. If you haven't received it, first check your spam or junk folder. Then, log in to your Amazon account and go to 'Your Orders'. Select the order in question and look for the option to resend the confirmation email. If you don't see this option, please contact Amazon Customer Service, and they will be able to assist you further."
        },
        {
            "question": "My order confirmation is missing some details; what should I do?",
            "answer": "If your order confirmation email is missing some details, follow these steps:\n1. Log in to your Amazon account and go to 'Your Orders'.\n2. Select the order in question to view the complete details.\n3. If the details are still missing or appear incorrect, contact Amazon Customer Service for assistance. They can verify the information and provide you with the correct order details. Rest assured, Amazon's Customer Service team is here to help resolve any issues you may encounter with your order confirmation."
        }
    ],

    "Delayed Refunds": [
        {
            "question": "Why is my refund taking so long?",
            "answer": "There are several factors that can cause delays in processing refunds on Amazon. These include the payment method used, the time it takes for the returned item to reach our fulfillment center, and the time required to inspect the returned item. Additionally, banks and credit card companies may take several business days to process the refund once it has been issued by Amazon. Rest assured, we are working diligently to process your refund as quickly as possible."
        },
        {
            "question": "When can I expect to receive my refund?",
            "answer": "The timeframe for receiving your refund depends on the payment method used and the processing times of your bank or credit card company. Typically, refunds are processed within 3-5 business days after we receive and inspect the returned item. However, it may take an additional 5-7 business days for the refund to appear in your account. You can check the status of your refund in the 'Your Orders' section of your Amazon account."
        },
        {
            "question": "What should I do if my refund is delayed?",
            "answer": "If your refund is delayed, please take the following steps:\n1. Check the status of your refund in the 'Your Orders' section of your Amazon account.\n2. Verify that the returned item has been received and inspected by our fulfillment center.\n3. Contact your bank or credit card company to inquire about their processing times for refunds.\n4. If you have completed these steps and still haven't received your refund, please contact Amazon Customer Service for further assistance. We are here to help resolve any issues you may encounter."
        },
        {
            "question": "How long does it usually take to process a refund?",
            "answer": "Refund processing times vary based on the payment method used and the policies of your bank or credit card company. Generally, once we receive and inspect the returned item, we process the refund within 3-5 business days. After that, it may take an additional 5-7 business days for the refund to appear in your account. If you used a credit card, it might take up to a billing cycle for the refund to be reflected on your statement."
        },
        {
            "question": "Can you expedite my refund process?",
            "answer": "We understand the urgency of receiving your refund quickly. While we strive to process all refunds as quickly as possible, there are certain steps that need to be followed, including receiving and inspecting the returned item. If you believe your refund is taking longer than expected, please contact Amazon Customer Service. We can review your case and see if there are any steps we can take to expedite the process."
        },
        {
            "question": "What are the steps to check the status of my refund?",
            "answer": "To check the status of your refund, follow these steps:\n1. Log in to your Amazon account.\n2. Go to 'Your Orders'.\n3. Find the order associated with the refund and select 'View order details'.\n4. Look for the refund status information, which will indicate whether the refund is being processed or has been completed.\nIf you need more detailed information, please contact Amazon Customer Service for further assistance."
        },
        {
            "question": "My refund hasn't appeared in my account yet; what should I do?",
            "answer": "If your refund hasn't appeared in your account yet, follow these steps:\n1. Verify the status of your refund in the 'Your Orders' section of your Amazon account.\n2. Check with your bank or credit card company to see if the refund is pending.\n3. Allow up to 7 business days for the refund to be processed by your bank or credit card company.\n4. If you still haven't received your refund after taking these steps, please contact Amazon Customer Service for further assistance. We are here to help ensure that your refund is processed correctly and promptly."
        }
    ],

    "Security Concern": [
        {
            "question": "How secure is my payment information?",
            "answer": "Your payment information is highly secure on Amazon. We use advanced encryption methods and security protocols to protect your data. All payment transactions are processed through secure servers using SSL (Secure Socket Layer) encryption, which ensures that your information is transmitted securely. Additionally, we adhere to strict compliance standards, including PCI DSS (Payment Card Industry Data Security Standard), to protect your payment details."
        },
        {
            "question": "What measures are in place to protect my payment details?",
            "answer": "Amazon employs multiple security measures to protect your payment details, including:\n1. SSL encryption: All payment information is encrypted using SSL technology during transmission.\n2. Tokenization: Sensitive card information is replaced with unique tokens to reduce the risk of fraud.\n3. Fraud detection systems: Advanced algorithms and machine learning are used to detect and prevent fraudulent transactions.\n4. Two-factor authentication: Optional two-step verification adds an extra layer of security to your account.\n5. Regular security audits: We conduct frequent security audits and updates to maintain the highest level of security for your data."
        },
        {
            "question": "I suspect a security breach; what should I do?",
            "answer": "If you suspect a security breach, take the following steps immediately:\n1. Change your Amazon account password: Go to 'Your Account' > 'Login & security' and update your password.\n2. Enable two-step verification: Add an extra layer of security to your account by enabling two-step verification under 'Login & security'.\n3. Review recent transactions: Check your order history and payment methods for any unauthorized activity.\n4. Contact your bank: Inform your bank or credit card issuer of any suspicious transactions and follow their guidance.\n5. Report to Amazon: Contact Amazon Customer Service to report the suspected breach and receive further assistance."
        },
        {
            "question": "How can I ensure my payment is secure?",
            "answer": "To ensure your payment is secure on Amazon, follow these best practices:\n1. Use strong passwords: Create a strong, unique password for your Amazon account and change it regularly.\n2. Enable two-step verification: Add an extra layer of security to your account by enabling two-step verification under 'Login & security'.\n3. Monitor your account: Regularly review your order history and payment methods for any unauthorized activity.\n4. Avoid public Wi-Fi: When making purchases, use a secure and private internet connection instead of public Wi-Fi.\n5. Keep your software updated: Ensure your device's operating system, browser, and antivirus software are up to date to protect against security vulnerabilities."
        },
        {
            "question": "Are my credit card details safe on your platform?",
            "answer": "Yes, your credit card details are safe on Amazon. We use advanced encryption methods and security protocols to protect your payment information. All transactions are processed through secure servers using SSL (Secure Socket Layer) encryption, and we adhere to strict compliance standards, including PCI DSS (Payment Card Industry Data Security Standard). Additionally, sensitive card information is tokenized to further enhance security. Rest assured, we take the protection of your payment details very seriously."
        },
        {
            "question": "What should I do if I notice unauthorized transactions?",
            "answer": "If you notice unauthorized transactions on your Amazon account, take the following steps immediately:\n1. Change your Amazon account password: Go to 'Your Account' > 'Login & security' and update your password.\n2. Enable two-step verification: Add an extra layer of security to your account by enabling two-step verification under 'Login & security'.\n3. Review recent transactions: Check your order history and payment methods for any unauthorized activity.\n4. Contact your bank: Inform your bank or credit card issuer of any suspicious transactions and follow their guidance.\n5. Report to Amazon: Contact Amazon Customer Service to report the unauthorized transactions and receive further assistance."
        },
        {
            "question": "How can I report a security concern related to my payment?",
            "answer": "To report a security concern related to your payment on Amazon, follow these steps:\n1. Contact Amazon Customer Service: Visit the Amazon Customer Service page and select 'Contact Us'. Choose the relevant issue and describe your security concern in detail.\n2. Provide necessary details: Be prepared to provide information such as order numbers, payment method details, and any suspicious activity you have noticed.\n3. Follow up: Amazon's security team will investigate the issue and may contact you for additional information. Ensure you follow their instructions and provide any requested information promptly.\n4. Monitor your account: Regularly review your order history and payment methods for any further unauthorized activity and update your security settings as needed."
        }
    ],

    "International Payments": [
        {
            "question": "Can I make an international payment?",
            "answer": "Yes, you can make international payments on Amazon. We accept a variety of payment methods from different countries. When you place an order, you can use internationally recognized credit or debit cards, and other global payment methods available in your region. If you're shopping on an Amazon website for a different country, you may need to create an account for that specific site."
        },
        {
            "question": "What are the fees for international payments?",
            "answer": "The fees for international payments can vary based on your payment method and your bank's policies. Amazon does not charge additional fees for processing international payments. However, your bank or credit card issuer may charge foreign transaction fees or currency conversion fees. It's best to check with your bank or card issuer to understand any potential charges before making an international purchase."
        },
        {
            "question": "How do I make a payment from abroad?",
            "answer": "To make a payment from abroad on Amazon, follow these steps:\n1. Log in to your Amazon account.\n2. Browse and add items to your cart.\n3. Proceed to checkout and enter your shipping address.\n4. Select your preferred payment method. You can use international credit or debit cards, and other globally accepted payment methods.\n5. Review your order details, including the total cost and estimated delivery date.\n6. Confirm your payment to complete the purchase.\nIf you encounter any issues, ensure your payment method supports international transactions and contact your bank if necessary."
        },
        {
            "question": "Are there any restrictions on international payments?",
            "answer": "While Amazon accepts many international payment methods, there may be some restrictions depending on the country you are purchasing from or shipping to. Certain products may not be eligible for international shipping, and some payment methods may not be accepted in all regions. Additionally, your bank or credit card issuer may have restrictions on international transactions. To avoid any issues, ensure that your payment method supports international payments and that the items you wish to purchase can be shipped to your location."
        },
        {
            "question": "How long do international payments take to process?",
            "answer": "International payments on Amazon are typically processed immediately, just like domestic payments. However, the actual time it takes for the payment to reflect in your account can vary depending on your bank or credit card issuer. In most cases, the payment should appear on your statement within a few business days. If you encounter any delays, please contact your bank or credit card issuer for more information."
        },
        {
            "question": "What currencies are supported for international payments?",
            "answer": "Amazon supports payments in a variety of currencies depending on the country-specific Amazon website you are using. When you shop on Amazon, the prices will be displayed in the local currency of the website you are visiting. During the checkout process, you will see the total amount in the local currency before you confirm your payment. If you are using a credit or debit card, your bank will handle the currency conversion and may charge a fee for this service."
        },
        {
            "question": "Why is my international payment not going through?",
            "answer": "If your international payment is not going through, consider the following potential issues:\n1. Incorrect payment details: Double-check your card number, expiration date, and CVV.\n2. Insufficient funds: Ensure you have enough funds in your account to cover the purchase.\n3. Card restrictions: Your bank or credit card issuer may have restrictions on international transactions. Contact your bank to confirm.\n4. Network issues: Temporary network problems can affect payment processing. Wait a few minutes and try again.\n5. Unsupported payment method: Ensure that your payment method is accepted for international transactions on Amazon.\nIf you continue to experience issues, please contact Amazon Customer Service for further assistance."
        }
    ],

    
    "Hidden Fees": [
        {
            "question": "Are there any hidden fees I should be aware of?",
            "answer": "Amazon strives to maintain transparency in pricing, and we do not charge hidden fees. However, there may be additional charges such as taxes, shipping fees, or import duties depending on your location and the items you purchase. These charges are typically displayed during the checkout process before you confirm your order. If you are using an international payment method, your bank or credit card issuer might charge foreign transaction fees or currency conversion fees. Please review all costs during checkout and consult your bank for any additional fees they may impose."
        },
        {
            "question": "Why was I charged an additional fee?",
            "answer": "Additional fees may arise from various sources. Common reasons include taxes, shipping fees, and import duties based on your location and the items purchased. These charges are usually displayed during the checkout process. If the additional fee was not mentioned at checkout, it could be a foreign transaction fee or currency conversion fee charged by your bank or credit card issuer. To understand the exact reason for the additional fee, please review your order details and consult your bank if necessary."
        },
        {
            "question": "How can I find out about all the fees associated with my payment?",
            "answer": "To find out about all the fees associated with your payment on Amazon, follow these steps:\n1. During the checkout process, review the order summary, which includes item prices, taxes, shipping fees, and any applicable import duties.\n2. Check the payment method details for any additional charges like foreign transaction fees or currency conversion fees from your bank or credit card issuer.\n3. After placing your order, you can view the detailed breakdown of charges in the 'Your Orders' section of your Amazon account.\n4. If you have any questions about specific charges, please contact Amazon Customer Service for assistance."
        },
        {
            "question": "Can you explain the extra charges on my bill?",
            "answer": "Certainly! Extra charges on your bill may include taxes, shipping fees, and import duties based on your location and the items you purchased. These charges are usually displayed during the checkout process. If you see unexpected extra charges, they might be foreign transaction fees or currency conversion fees from your bank or credit card issuer. To get a detailed explanation of the charges on your bill, please review your order summary in the 'Your Orders' section of your Amazon account or contact Amazon Customer Service for further assistance."
        },
        {
            "question": "How can I avoid hidden fees?",
            "answer": "To avoid hidden fees when shopping on Amazon, follow these tips:\n1. Review your order summary during the checkout process to see all applicable charges, including taxes, shipping fees, and import duties.\n2. Use a payment method that does not charge foreign transaction fees or currency conversion fees, or check with your bank about potential charges.\n3. Ensure that the shipping address is correct to avoid additional charges for incorrect or failed deliveries.\n4. Purchase items from local sellers or those who offer free shipping to minimize additional shipping costs.\n5. Contact Amazon Customer Service if you have any questions about potential fees before completing your purchase."
        },
        {
            "question": "What are the common hidden fees in my transactions?",
            "answer": "Common hidden fees in transactions can include:\n1. Foreign transaction fees: Charged by your bank or credit card issuer for purchases made from international sellers.\n2. Currency conversion fees: Applied by your bank when converting currencies for international purchases.\n3. Import duties and taxes: Levied by your country's customs for items shipped from abroad.\n4. Shipping fees: Additional charges for expedited or international shipping.\n5. Return shipping fees: Costs associated with returning an item.\nTo minimize these fees, review the order summary during checkout and consult your bank about any fees they may impose."
        },
        {
            "question": "Why is there a discrepancy between the amount I paid and the amount charged?",
            "answer": "A discrepancy between the amount you paid and the amount charged can occur due to several reasons:\n1. Taxes and import duties: These charges may be applied based on your location and the items purchased.\n2. Shipping fees: Additional costs for expedited or international shipping.\n3. Foreign transaction fees: Charged by your bank or credit card issuer for international purchases.\n4. Currency conversion fees: Applied by your bank when converting currencies.\n5. Promotional discounts: If a discount was applied, the final amount charged may differ from the initial total.\nPlease review your order summary and contact Amazon Customer Service or your bank for a detailed explanation of the charges."
        }
    ],

"Transaction Limit": [
        {
            "question": "What is the maximum transaction limit?",
            "answer": "The maximum transaction limit on Amazon can vary based on the payment method you use and the policies of your bank or credit card issuer. Typically, there is no specific limit set by Amazon, but individual banks and credit card companies may impose their own limits on transaction amounts. To find out the exact limit, please check with your bank or credit card issuer."
        },
        {
            "question": "Can I increase my transaction limit?",
            "answer": "To increase your transaction limit, you will need to contact your bank or credit card issuer directly. They can provide information on your current limit and guide you through the process of requesting an increase. In some cases, you may need to provide additional information or documentation to support your request."
        },
        {
            "question": "Why was my transaction declined due to a limit?",
            "answer": "Your transaction may have been declined due to reaching your bank or credit card issuer's transaction limit. Each financial institution has its own policies and limits on the amount you can spend per transaction or per day. To resolve this, please contact your bank or credit card issuer to verify your current limit and discuss options for increasing it if necessary."
        },
        {
            "question": "How can I check my current transaction limit?",
            "answer": "To check your current transaction limit, you will need to contact your bank or credit card issuer. They can provide you with information about your account's spending limits, including any daily, weekly, or per-transaction limits. You can usually find this information by logging into your online banking account or by calling your bank's customer service."
        },
        {
            "question": "Are there different limits for different payment methods?",
            "answer": "Yes, different payment methods can have different transaction limits. For example, credit cards, debit cards, and digital wallets may each have their own set of limits imposed by the issuing bank or financial institution. Additionally, some banks may have higher limits for certain types of cards or accounts. To get detailed information about the limits for your specific payment method, please contact your bank or payment provider."
        },
        {
            "question": "What should I do if I need to make a payment above my limit?",
            "answer": "If you need to make a payment that exceeds your current transaction limit, consider the following options:\n1. Contact your bank or credit card issuer to request a temporary or permanent increase in your transaction limit.\n2. Split your purchase into multiple smaller transactions if possible.\n3. Use an alternative payment method that has a higher limit.\n4. Consider using a combination of payment methods to cover the total amount.\nIf you need further assistance, please contact Amazon Customer Service for support."
        },
        {
            "question": "How often are transaction limits updated?",
            "answer": "Transaction limits are typically set by your bank or credit card issuer and can be updated based on their internal policies and your account usage. Some banks may review and adjust limits periodically, while others may only change limits upon request. To understand how often your transaction limits are updated, please contact your bank or credit card issuer directly."
        }
    ],

    "Loyalty Points and Gift Cards": [
        {
            "question": "How can I redeem my loyalty points?",
            "answer": "To redeem your loyalty points on Amazon, follow these steps:\n1. Ensure you are logged in to your Amazon account.\n2. Add the items you wish to purchase to your cart.\n3. Proceed to checkout and select your payment method.\n4. On the payment page, you will see an option to apply your loyalty points to the order. Select this option to use your points.\n5. Complete the checkout process.\nIf you have any issues redeeming your points, please contact Amazon Customer Service for assistance."
        },
        {
            "question": "Can I use multiple gift cards for a single purchase?",
            "answer": "Yes, you can use multiple gift cards for a single purchase on Amazon. During the checkout process, you can enter the claim codes for each gift card you wish to apply. The total value of the gift cards will be combined and applied to your order. If the total amount of the gift cards exceeds the purchase amount, the remaining balance will be stored in your Amazon account for future use."
        },
        {
            "question": "How do I check my loyalty points balance?",
            "answer": "To check your loyalty points balance on Amazon, follow these steps:\n1. Log in to your Amazon account.\n2. Go to 'Your Account' and select 'Your Payments'.\n3. Click on 'Reward Points' to view your current points balance and transaction history.\nIf you have any issues accessing your points balance, please contact Amazon Customer Service for assistance."
        },
        {
            "question": "What can I purchase with my gift cards?",
            "answer": "Amazon gift cards can be used to purchase millions of items available on Amazon, including books, electronics, clothing, household items, and more. You can also use gift cards to pay for digital content such as Kindle books, Amazon Music, and Amazon Prime memberships. However, gift cards cannot be used to purchase other gift cards or certain third-party gift cards available on Amazon."
        },
        {
            "question": "Are there any restrictions on using loyalty points?",
            "answer": "While loyalty points can be used for most purchases on Amazon, there are a few restrictions:\n1. Loyalty points cannot be used to purchase other gift cards.\n2. Some digital content and subscriptions may not be eligible for payment with loyalty points.\n3. Points may not be transferable and are usually tied to the account that earned them.\n4. Specific promotional points may have expiration dates or additional terms and conditions.\nPlease review the terms and conditions of your loyalty points program for any specific restrictions."
        },
        {
            "question": "How long are gift cards valid for?",
            "answer": "Amazon gift cards typically do not have an expiration date and can be used at any time. However, it is always a good idea to check the terms and conditions of your specific gift card to confirm its validity. If you have any concerns about the expiration of your gift card, please contact Amazon Customer Service for more information."
        },
        {
            "question": "Why can't I apply my loyalty points at checkout?",
            "answer": "If you are unable to apply your loyalty points at checkout, consider the following potential issues:\n1. Ensure you are logged in to the correct Amazon account that holds the loyalty points.\n2. Check if the items in your cart are eligible for purchase with loyalty points. Some items, such as other gift cards or certain digital content, may not be eligible.\n3. Verify that your points balance is sufficient to cover part or all of the purchase.\n4. Ensure that the option to apply points is selected during the payment process.\nIf you still cannot apply your points, please contact Amazon Customer Service for assistance."
        }
    ],

    "Promo Codes and Discount Issues": [
        {
            "question": "Why isn't my promo code working?",
            "answer": "There could be several reasons why your promo code isn't working:\n1. Expired Code: Check the expiration date of the promo code to ensure it is still valid.\n2. Eligibility: Ensure that the items in your cart are eligible for the promo code. Some codes are only valid for specific products or categories.\n3. Minimum Purchase Requirement: Some promo codes require a minimum purchase amount. Verify that your order meets this requirement.\n4. Typing Error: Double-check the promo code for any typing errors. Promo codes are case-sensitive and must be entered exactly as provided.\n5. Single Use: Some promo codes can only be used once per customer. If you have used the code previously, it will not work again.\nIf you continue to experience issues, please contact Amazon Customer Service for further assistance."
        },
        {
            "question": "How can I apply a promo code to my purchase?",
            "answer": "To apply a promo code to your purchase on Amazon, follow these steps:\n1. Add the eligible items to your cart.\n2. Proceed to checkout.\n3. On the 'Review your order' page, you will see a section labeled 'Gift Cards & Promotional Codes'.\n4. Enter the promo code in the provided field and click 'Apply'.\n5. Ensure that the discount has been applied before completing your purchase.\nIf you encounter any issues, please contact Amazon Customer Service for assistance."
        },
        {
            "question": "Can I use more than one promo code at a time?",
            "answer": "Amazon's policy generally allows only one promo code to be applied per order. If you have multiple promo codes, you will need to choose the one that offers the best discount for your purchase. Be sure to review the terms and conditions of each promo code, as some codes may have specific restrictions or limitations."
        },
        {
            "question": "What should I do if my discount wasn't applied?",
            "answer": "If your discount wasn't applied, follow these steps:\n1. Verify that the promo code was entered correctly and is still valid.\n2. Ensure that the items in your cart are eligible for the promo code.\n3. Check if there are any minimum purchase requirements that you may not have met.\n4. Try re-entering the promo code and applying it again.\n5. If the discount still doesn't apply, please contact Amazon Customer Service for assistance. Provide them with the promo code and order details, and they will help resolve the issue."
        },
        {
            "question": "Are there any restrictions on using promo codes?",
            "answer": "Yes, there are typically restrictions on using promo codes, which may include:\n1. Expiration Dates: Promo codes are often valid for a limited time and expire after a certain date.\n2. Eligibility: Some promo codes are only valid for specific products, categories, or brands.\n3. Single Use: Many promo codes can only be used once per customer or account.\n4. Minimum Purchase Requirements: Some promo codes require a minimum purchase amount to be applied.\n5. Combination: Promo codes usually cannot be combined with other discounts or promotions.\nBe sure to review the terms and conditions of each promo code to understand any specific restrictions."
        },
        {
            "question": "How do I find available promo codes and discounts?",
            "answer": "To find available promo codes and discounts on Amazon, you can:\n1. Visit the Amazon 'Today's Deals' page for current promotions and discounts.\n2. Subscribe to Amazon's email newsletters to receive notifications about special offers and promo codes.\n3. Check the 'Coupons' section on Amazon for available coupons that can be applied to your orders.\n4. Follow Amazon on social media platforms where they may share exclusive promo codes and deals.\n5. Look for promo codes on third-party coupon websites, but always verify their validity before use."
        },
        {
            "question": "Why was my promo code rejected?",
            "answer": "A promo code may be rejected for several reasons:\n1. Expiration: The promo code has expired and is no longer valid.\n2. Eligibility: The items in your cart are not eligible for the promo code.\n3. Minimum Purchase: Your order does not meet the minimum purchase requirement for the promo code.\n4. Single Use: The promo code has already been used and cannot be applied again.\n5. Typing Error: There may be a mistake in how the promo code was entered. Ensure it is entered exactly as provided.\n6. Combination: The promo code cannot be combined with other discounts or promotions.\nIf you are unsure why the promo code was rejected, please contact Amazon Customer Service for assistance."
        }
    ],
    
    "Complex Checkout Process": [
        {
            "question": "Why is the checkout process so complicated?",
            "answer": "The checkout process is designed to ensure the security of your purchase and to verify your details accurately. However, we are constantly working to streamline it for a smoother experience."
        },
        {
            "question": "Can you simplify the steps to complete my purchase?",
            "answer": "Absolutely! We're committed to making your shopping experience as seamless as possible. We'll review our checkout process to see where we can simplify and enhance it."
        },
        {
            "question": "What information do I need to complete the checkout?",
            "answer": "You'll typically need your shipping address, payment information, and contact details. Rest assured, all information is kept secure and confidential."
        },
        {
            "question": "How can I speed up the checkout process?",
            "answer": "You can create an account to save your details for future purchases. Additionally, ensuring your information is up-to-date can expedite the process."
        },
        {
            "question": "Why do I need to enter so much information at checkout?",
            "answer": "We require essential information to ensure accurate delivery and secure transactions. Your privacy and security are our top priorities."
        },
        {
            "question": "Can I save my details to make checkout faster next time?",
            "answer": "Yes, you can! Creating an account allows you to securely store your information, making future checkouts quicker and easier."
        },
        {
            "question": "What should I do if I get stuck during checkout?",
            "answer": "If you encounter any issues during checkout, our customer service team is here to help. Simply reach out to us via phone, chat, or email, and we'll assist you promptly."
        }
    ],

    "Payment Options": [
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept various payment methods including credit cards (Visa, MasterCard, American Express), debit cards, Amazon Pay, PayPal, and more. You can view all available options during checkout."
        },
        {
            "question": "Can I pay with a credit card?",
            "answer": "Yes, you can pay with a credit card. We accept Visa, MasterCard, American Express, and other major credit cards."
        },
        {
            "question": "Is there an option to pay with a mobile wallet?",
            "answer": "Yes, you can pay with mobile wallets like Amazon Pay, Apple Pay, Google Pay, and Samsung Pay, depending on availability."
        },
        {
            "question": "How can I add a new payment method?",
            "answer": "To add a new payment method, go to 'Your Account' > 'Payment options'. From there, you can add, edit, or remove payment methods as needed."
        },
        {
            "question": "Are there any payment methods that offer discounts?",
            "answer": "Occasionally, certain payment methods or promotions may offer discounts. Check the 'Payment options' section during checkout for any available discounts."
        },
        {
            "question": "Can I split my payment across multiple methods?",
            "answer": "Currently, we do not support splitting payments across multiple methods for a single order. You can use one payment method per transaction."
        },
        {
            "question": "Why isn't my preferred payment option available?",
            "answer": "There could be several reasons why your preferred payment option isn't available, such as regional restrictions, account issues, or temporary service interruptions. We recommend checking alternative payment methods or contacting customer service for assistance."
        }
    ],

    "EMI & Installments": [
        {
            "question": "Do you offer EMI or installment payment options?",
            "answer": "Yes, we offer EMI (Equated Monthly Installments) and installment payment options on eligible products. These options may vary based on the item and your location."
        },
        {
            "question": "How can I choose to pay in installments?",
            "answer": "During checkout, if your purchase is eligible for installment payments, you will see the option to 'Pay in installments' or 'EMI' depending on availability. You can then select this option and proceed."
        },
        {
            "question": "What are the terms and conditions for EMI payments?",
            "answer": "EMI terms and conditions vary based on the bank or financial institution providing the service. Typically, there may be interest charges and a minimum purchase amount required. Please review the specific terms during checkout."
        },
        {
            "question": "Is there any interest on installment payments?",
            "answer": "Yes, installment payments may accrue interest depending on the EMI plan and the terms set by the bank or financial institution. The interest rate and other charges will be displayed during checkout."
        },
        {
            "question": "Can I pay off my EMI early?",
            "answer": "Yes, you can usually pay off your EMI early. However, you should check with your bank or financial institution for any prepayment charges or penalties that may apply."
        },
        {
            "question": "How do I check the remaining balance on my installment plan?",
            "answer": "You can usually check the remaining balance of your installment plan by logging into your bank account or contacting your bank directly. They will provide you with the current status of your EMI payments."
        },
        {
            "question": "Why was my EMI request declined?",
            "answer": "EMI requests can be declined due to various reasons such as insufficient credit limit, eligibility criteria not met, or technical issues. We recommend contacting your bank or financial institution for specific details on why your EMI request was declined."
        }
    ],

    "Confusing Payment Options": [
        {
            "question": "How do I select the best payment option for me?",
            "answer": "To select the best payment option, consider factors such as convenience, security, any available discounts or rewards, and your personal preferences. Review the details of each payment method available during checkout to make an informed choice."
        },
        {
            "question": "What are the differences between the payment options available?",
            "answer": "Payment options vary in terms of acceptance, security features, convenience, and any associated fees or rewards. Credit cards offer flexibility and rewards, while debit cards deduct funds directly from your account. Mobile wallets like Apple Pay and Google Pay provide quick and secure transactions."
        },
        {
            "question": "Can you explain the benefits of each payment method?",
            "answer": "Certainly! Credit cards offer benefits such as rewards points and purchase protection. Debit cards provide direct access to funds without accruing debt. Mobile wallets offer convenience and security with features like fingerprint authentication. Each method has unique advantages tailored to different customer needs."
        },
        {
            "question": "Why are there so many payment options?",
            "answer": "We provide multiple payment options to accommodate diverse customer preferences and ensure convenience. This allows you to choose the method that best suits your needs, whether it's credit cards, debit cards, mobile wallets, or other options."
        },
        {
            "question": "How can I change my selected payment option?",
            "answer": "If you wish to change your selected payment option before completing your order, you can usually do so by going back to the payment method section during checkout. Select a different payment method that meets your preferences."
        },
        {
            "question": "Which payment option is the most secure?",
            "answer": "Security measures vary by payment method, but generally, credit cards and reputable mobile wallets offer strong security features such as encryption and fraud detection. It's important to use secure networks and devices when making transactions online."
        },
        {
            "question": "Why is my preferred payment option not recommended?",
            "answer": "Your preferred payment option may not be recommended for reasons such as regional availability, security concerns, or compatibility issues with our payment processing system. We strive to recommend the most secure and reliable options based on your location and transaction details."
        }
    ]
}

for category, questions in query_category.items():
    # pinecone_vector_store(questions, category)
    document_split(questions, category)
    break
