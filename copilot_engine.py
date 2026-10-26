"""
Paytm VyaparAI — Autonomous Merchant Copilot Engine
Multi-Language Support: English, Telugu, Hindi, Tamil, Kannada
"""

import datetime
from typing import Dict, List, Any

class MerchantCopilotEngine:
    def __init__(self):
        self.merchant_profile = {
            "store_name": "Gupta Kirana & General Store",
            "owner": "Ramesh Gupta",
            "location": "Koramangala 4th Block, Bengaluru",
            "upi_id": "guptakirana@paytm",
            "soundbox_id": "SB-BLR-89211",
            "soundbox_status": "ONLINE",
            "account_balance": 48250.00
        }

        # Simulated transactions
        self.transactions = [
            {"id": "TXN101", "time": "08:15 AM", "customer": "Walk-in", "amount": 60, "items": ["Amul Taaza Milk 500ml (2)"]},
            {"id": "TXN102", "time": "09:30 AM", "customer": "Sunil K", "amount": 250, "items": ["Tata Tea Gold 250g", "Sugar 1kg"]},
            {"id": "TXN103", "time": "11:20 AM", "customer": "Neha P", "amount": 120, "items": ["Thums Up 750ml (2)"]},
            {"id": "TXN104", "time": "01:45 PM", "customer": "Walk-in", "amount": 450, "items": ["Fortune Sunlite Oil 1L", "Aashirvaad Atta 5kg"]},
            {"id": "TXN105", "time": "04:10 PM", "customer": "Dr. Verma", "amount": 180, "items": ["Dettol Soap 3pk", "Colgate Paste"]},
            {"id": "TXN106", "time": "06:30 PM", "customer": "Rahul M", "amount": 340, "items": ["Amul Butter 100g", "Bread", "Eggs 6pk"]},
            {"id": "TXN107", "time": "07:15 PM", "customer": "Priya S", "amount": 90, "items": ["Maggi 4pk"]},
        ]

        # Inventory SKU Database
        self.inventory = [
            {"sku": "AMUL-MILK-500", "name": "Amul Taaza Milk 500ml", "category": "Dairy", "stock": 4, "reorder_threshold": 15, "cost_price": 24.5, "mrp": 27.0, "daily_velocity": 35},
            {"sku": "THUMS-750", "name": "Thums Up 750ml", "category": "Beverages", "stock": 8, "reorder_threshold": 20, "cost_price": 36.0, "mrp": 45.0, "daily_velocity": 22},
            {"sku": "AMUL-BTR-100", "name": "Amul Butter 100g", "category": "Dairy", "stock": 6, "reorder_threshold": 12, "cost_price": 51.0, "mrp": 58.0, "daily_velocity": 14},
            {"sku": "TATA-TEA-250", "name": "Tata Tea Gold 250g", "category": "Beverages", "stock": 25, "reorder_threshold": 10, "cost_price": 135.0, "mrp": 160.0, "daily_velocity": 6},
            {"sku": "AASHIR-ATTA-5", "name": "Aashirvaad Atta 5kg", "category": "Staples", "stock": 18, "reorder_threshold": 8, "cost_price": 240.0, "mrp": 275.0, "daily_velocity": 5},
            {"sku": "FORT-OIL-1L", "name": "Fortune Sunflower Oil 1L", "category": "Edible Oils", "stock": 15, "reorder_threshold": 10, "cost_price": 125.0, "mrp": 145.0, "daily_velocity": 8},
            {"sku": "STAG-CHIPS-X", "name": "Brand X Nachos 100g", "category": "Snacks", "stock": 35, "reorder_threshold": 5, "cost_price": 40.0, "mrp": 50.0, "daily_velocity": 0.2, "status": "STAGNANT"}
        ]

        # Khata (Udhar / Credit) Ledger
        self.khata = [
            {"id": "K1", "name": "Ramesh Sharma", "phone": "+91 98765 43210", "due_amount": 3420, "days_pending": 12, "last_reminder": "2 days ago", "notes": "Groceries & Cooking Oil"},
            {"id": "K2", "name": "Sita Ram Tailor", "phone": "+91 98111 22334", "due_amount": 1180, "days_pending": 5, "last_reminder": "Never", "notes": "Daily tea milk & biscuits"},
            {"id": "K3", "name": "Anil Verma Gym", "phone": "+91 98450 99887", "due_amount": 4850, "days_pending": 18, "last_reminder": "5 days ago", "notes": "Eggs tray, bananas & oats"},
            {"id": "K4", "name": "Pooja Reddy", "phone": "+91 97333 44556", "due_amount": 950, "days_pending": 3, "last_reminder": "Never", "notes": "Snacks & soft drinks"},
            {"id": "K5", "name": "Kiran Kumar", "phone": "+91 99000 11223", "due_amount": 2050, "days_pending": 9, "last_reminder": "3 days ago", "notes": "Monthly staples"}
        ]

        # Hyper-local 2km Neighborhood Demand Signals
        self.hyperlocal_trends = [
            {"trend": "Cold Drinks & Hydration", "change": "+44%", "reason": "Heatwave trigger: Temperatures +3.5°C above seasonal normal", "action": "Increase inventory buffer by 30 units."},
            {"trend": "Pooja Flowers & Camphor", "change": "+32%", "reason": "Upcoming Ekadashi & weekend temple footfall", "action": "Pre-order 20 packets from regional distributor."},
            {"trend": "Stagnant Stock Alert", "change": "-60%", "reason": "Brand X Nachos has 0 sales in 14 days", "action": "Bundle with Thums Up at 10% discount to unlock trapped cash."}
        ]

        # ONDC Wholesale Distributors
        self.ondc_distributors = [
            {"name": "Sri Balaji Dairy Agency", "distance_km": 1.2, "rating": 4.8, "sku": "AMUL-MILK-500", "wholesale_price": 24.2, "delivery_eta": "45 mins"},
            {"name": "Metro Cash & Carry ONDC", "distance_km": 3.8, "rating": 4.6, "sku": "THUMS-750", "wholesale_price": 35.5, "delivery_eta": "90 mins"},
            {"name": "Karnataka Dairy Federation ONDC", "distance_km": 2.1, "rating": 4.7, "sku": "AMUL-BTR-100", "wholesale_price": 50.5, "delivery_eta": "60 mins"}
        ]

    # Multilingual Voice Responses
    def _get_response_text(self, intent: str, lang: str, **kwargs) -> str:
        lang = lang.lower().strip()
        
        if intent == "SALES_SUMMARY":
            total = kwargs.get("total", "18,420")
            count = kwargs.get("count", "64")
            top_item = kwargs.get("top_item", "Amul Taaza Milk 500ml")

            if lang == "telugu":
                return f"సేత్ గారూ, ఈరోజు సాయంత్రం 7 గంటల వరకు మొత్తం ₹{total} కలెక్షన్ వచ్చింది ({count} లావాదేవీలు). అత్యధికంగా అమ్ముడైన వస్తువు '{top_item}'. జాగ్రత్త: అమూల్ పాలు కేవలం 4 ప్యాకెట్లు మాత్రమే మిగిలి ఉన్నాయి, వెంటనే రీస్టాక్ చేయండి!"
            elif lang == "tamil":
                return f"சேத் அவர்களே, இன்று மாலை 7 மணி வரை மொத்தம் ₹{total} வசூலாகியுள்ளது ({count} பரிவர்த்தனைகள்). அதிகம் விற்பனையான பொருள் '{top_item}'. கவனம்: அமுல் பால் வெறும் 4 பாக்கெட்டுகள் மட்டுமே உள்ளன, உடனே ரீஸ்டாக் செய்யுங்கள்!"
            elif lang == "kannada":
                return f"ಸೇಠ್ ಅವರೇ, ಇಂದು ಸಂಜೆ 7 ಗಂಟೆಯವರೆಗೆ ಒಟ್ಟು ₹{total} ಕಲೆಕ್ಷನ್ ಆಗಿದೆ ({count} ವಹಿವಾಟುಗಳು). ಅತಿ ಹೆಚ್ಚು ಮಾರಾಟವಾದ ವಸ್ತು '{top_item}'. ಗಮನಿಸಿ: ಅಮುಲ್ ಹಾಲಿನ ಕೇವಲ 4 ಪ್ಯಾಕೆಟ್‌ಗಳು ಉಳಿದಿವೆ, ತಕ್ಷಣವೇ ರೀಸ್ಟಾಕ್ ಮಾಡಿ!"
            elif lang == "hindi":
                return f"सेठ जी, आज शाम 7 बजे तक कुल ₹{total} का कलेक्शन हुआ है ({count} transactions). सबसे तेज़ बिकने वाला आइटम '{top_item}' रहा. ध्यान दें: अमूल दूध के सिर्फ 4 पैकेट बचे हैं, तुरंत रीस्टॉक करें!"
            else: # English
                return f"Boss, today's total collection reached ₹{total} across {count} transactions. The top-selling product was '{top_item}'. Alert: Amul Milk has only 4 packets left in stock, restock recommended immediately!"

        elif intent == "INVENTORY_CHECK":
            items = kwargs.get("items", "Amul Milk, Thums Up, Amul Butter")
            if lang == "telugu":
                return f"మీ దుకాణంలో 3 వస్తువులు తక్కువ స్టాక్‌లో ఉన్నాయి: {items}. శ్రీ బాలాజీ ఏజెన్సీ ONDC లో అమూల్ పాలను ₹24.20 కి ఇస్తున్నారు. 50 ప్యాకెట్ల రీ-ఆర్డర్ పెట్టమంటారా?"
            elif lang == "tamil":
                return f"உங்கள் கடையில் 3 பொருட்கள் குறைவான இருப்பில் உள்ளன: {items}. ஸ்ரீ பாலாஜி ஏஜென்சி ONDC-யில் அமுல் பாலை ₹24.20-க்கு வழங்குகிறது. 50 பாக்கெட்டுகளை ரீ-ஆர்டர் செய்யட்டுமா?"
            elif lang == "kannada":
                return f"ನಿಮ್ಮ ಅಂಗಡಿಯಲ್ಲಿ 3 ವಸ್ತುಗಳ ಸ್ಟಾಕ್ ಕಡಿಮೆಯಾಗಿದೆ: {items}. ಶ್ರೀ ಬಾಲಾಜಿ ಏಜೆನ್ಸಿ ONDC ಯಲ್ಲಿ ಅಮುಲ್ ಹಾಲನ್ನು ₹24.20 ಕ್ಕೆ ನೀಡುತ್ತಿದೆ. 50 ಪ್ಯಾಕೆಟ್‌ಗಳನ್ನು ಆರ್ಡರ್ ಮಾಡಲೇ?"
            elif lang == "hindi":
                return f"आपकी दुकान में 3 आइटम कम स्टॉक पर हैं: {items}. श्री बालाजी एजेंसी ONDC पर अमूल दूध ₹24.20 में दे रही है. क्या मैं 50 पैकेट का रीऑर्डर लगा दूं?"
            else: # English
                return f"You have 3 items running low on stock: {items}. Sri Balaji Agency on ONDC is offering Amul Milk at ₹24.20 (below retail). Should I place a 50-packet reorder?"

        elif intent == "KHATA_RECOVERY":
            due = kwargs.get("due", "12,450")
            name = kwargs.get("name", "Ramesh Sharma")
            cust_due = kwargs.get("cust_due", "3,420")
            days = kwargs.get("days", "12")

            if lang == "telugu":
                return f"దుకాణంలో 5 మంది కస్టమర్ల నుండి మొత్తం ₹{due} ఉధార్ బకాయి ఉంది. అత్యధికంగా {name} గారి వద్ద ₹{cust_due} బకాయి ఉంది ({days} రోజులుగా). వారి వాట్సాప్‌కు గౌరవప్రదమైన వాయిస్ రిమైండర్ మరియు పేటీఎం యూపీఐ లింక్ సిద్ధం చేశాను."
            elif lang == "tamil":
                return f"கடையில் 5 வாடிக்கையாளர்களிடம் மொத்தம் ₹{due} கடன் பாக்கி உள்ளது. அதிகபட்சமாக {name} அவர்களிடம் ₹{cust_due} பாக்கி உள்ளது ({days} நாட்களாக). அவரது வாட்ஸ்அப்பிற்கு கண்ணியமான நினைவூட்டல் மற்றும் பேடிஎம் யுபிஐ லிங்க் தயார் செய்துள்ளேன்."
            elif lang == "kannada":
                return f"ಅಂಗಡಿಯಲ್ಲಿ 5 ಗ್ರಾಹಕರಿಂದ ಒಟ್ಟು ₹{due} ಸಾಲದ ಹಣ ಬಾಕಿ ಇದೆ. ಗರಿಷ್ಠವಾಗಿ {name} ಅವರ ಬಳಿ ₹{cust_due} ಬಾಕಿ ಇದೆ ({days} ದಿನಗಳಿಂದ). ಅವರ ವಾಟ್ಸಾಪ್‌ಗೆ ವಿನಮ್ರ ವಾಯ್ಸ್ ರಿಮೈಂಡರ್ ಮತ್ತು ಪೇಟಿಎಂ ಯುಪಿಐ ಲಿಂಕ್ ಸಿದ್ಧಪಡಿಸಲಾಗಿದೆ."
            elif lang == "hindi":
                return f"दुकान पर कुल ₹{due} का उधार पेंडिंग है 5 ग्राहकों से. सबसे पुराना बैलेंस {name} जी का है: ₹{cust_due} ({days} दिनों से). मैंने उनके व्हाट्सएप पर विनम्र वॉयस रिमाइंडर और 1-क्लिक पेमेंट लिंक ड्राफ्ट कर दिया है."
            else: # English
                return f"A total of ₹{due} in customer credit (udhar) is pending across 5 customers. The highest balance is from {name}: ₹{cust_due} ({days} days pending). A polite reminder with 1-click Paytm UPI payment link has been drafted for WhatsApp."

        elif intent == "CREDIT_APPROVAL":
            limit = kwargs.get("limit", "2,50,000")
            if lang == "telugu":
                return f"అభినందనలు! మీ పేటీఎం సౌండ్‌బాక్స్ మరియు స్థిరమైన రోజువారీ యూపీఐ లావాదేవీల ఆధారంగా మీకు ₹{limit} తక్షణ వర్కింగ్ క్యాపిటల్ లోన్ ముందస్తుగా ఆమోదించబడింది. ఎటువంటి కాగితాలు లేకుండా 180 సెకన్లలో మీ ఖాతాకు జమ అవుతుంది."
            elif lang == "tamil":
                return f"வாழ்த்துகள்! உங்கள் பேடிஎம் சவுண்ட்பாக்ஸ் மற்றும் தினசரி யுபிஐ பரிவர்த்தனை வேகத்தின் அடிப்படையில் உங்களுக்கு ₹{limit} உடனடி மூலதன கடன் முன்அனுமதி வழங்கப்பட்டுள்ளது. எந்த ஆவணமும் இன்றி 180 வினாடிகளில் உங்கள் கணக்கில் சேரும்."
            elif lang == "kannada":
                return f"ಅಭಿನಂದನೆಗಳು! ನಿಮ್ಮ ಪೇಟಿಎಂ ಸೌಂಡ್‌ಬಾಕ್ಸ್ ಮತ್ತು ದೈನಂದಿನ ಯುಪಿಐ ವಹಿವಾಟುಗಳ ಆಧಾರದ ಮೇಲೆ ನಿಮಗೆ ₹{limit} ತ್ವರಿತ ವರ್ಕಿಂಗ್ ಕ್ಯಾಪಿಟಲ್ ಲೋನ್ ಅನುಮೋದಿಸಲಾಗಿದೆ. ಯಾವುದೇ ದಾಖಲೆಗಳಿಲ್ಲದೆ 180 ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಹಣ ಜಮೆಯಾಗಲಿದೆ."
            elif lang == "hindi":
                return f"बधाई हो सेठ जी! आपके वेरीफाइड पेटीएम साउंडबॉक्स और नियमित यूपीआई लेनदेन के आधार पर आपको ₹{limit} का इंस्टेंट वर्किंग कैपिटल लोन प्री-अप्रूव्ड मिला है. बिना किसी कागजी कार्रवाई के 180 सेकंड में आपके खाते में क्रेडिट हो जाएगा."
            else: # English
                return f"Congratulations! Based on your verified Paytm Soundbox and daily settlement velocity, you are pre-approved for ₹{limit} in instant working capital credit. Zero paperwork, disbursed in 180 seconds to your account."

        else: # GENERAL_ASSIST
            if lang == "telugu":
                return f"మీ అభ్యర్థన ప్రాసెస్ చేయబడింది. దుకాణం సజావుగా నడుస్తోంది. సౌండ్‌బాక్స్ 4.0 ఆన్‌లైన్‌లో ఉంది."
            elif lang == "tamil":
                return f"உங்கள் கோரிக்கை செயல்படுத்தப்பட்டது. கடை இயக்கம் சீராக உள்ளது. சவுண்ட்பாக்ஸ் 4.0 ஆன்லைனில் உள்ளது."
            elif lang == "kannada":
                return f"ನಿಮ್ಮ ವಿನಂತಿ ಪ್ರಕ್ರಿಯೆಗೊಂಡಿದೆ. ಅಂಗಡಿಯ ವಹಿವಾಟುಗಳು ಸುಗಮವಾಗಿ ನಡೆಯುತ್ತಿವೆ. ಸೌಂಡ್‌ಬಾಕ್ಸ್ 4.0 ಆನ್‌ಲೈನ್‌ನಲ್ಲಿದೆ."
            elif lang == "hindi":
                return f"आपकी दुकान का ऑपरेशन बिल्कुल सुचारू रूप से चल रहा है. साउंडबॉक्स 4.0 ऑनलाइन है."
            else: # English
                return f"Store operations are running smoothly. Soundbox 4.0 is online and active on your counter."

    # Process query with language support
    def process_query(self, query: str, language: str = "english") -> Dict[str, Any]:
        q_lower = query.lower().strip()
        lang = language.lower().strip()

        # Sales intent
        if any(w in q_lower for w in ["munafa", "collection", "today", "aaj", "sales", "earnings", "total", "లబ్ది", "కలెక్షన్", "வசூல்", "ಆದಾಯ"]):
            total_today = sum(t["amount"] for t in self.transactions) + 16930
            txn_count = len(self.transactions) + 57
            top_item = "Amul Taaza Milk 500ml"
            resp = self._get_response_text("SALES_SUMMARY", lang, total=f"{total_today:,}", count=str(txn_count), top_item=top_item)
            return {
                "intent": "SALES_SUMMARY",
                "language": lang,
                "voice_response": resp,
                "metrics": {
                    "total_sales": total_today,
                    "txn_count": txn_count,
                    "top_item": top_item,
                    "avg_ticket": round(total_today / txn_count, 1)
                },
                "recommended_action": {
                    "type": "RESTOCK_ALERT",
                    "text": "Restock 50 packets of Amul Milk via ONDC",
                    "sku": "AMUL-MILK-500"
                }
            }

        # Inventory intent
        elif any(w in q_lower for w in ["stock", "khatam", "order", "inventory", "reorder", "milk", "butter", "స్టాక్", "இருப்பு", "ದಾಸ್ತಾನು"]):
            low_stock = [item for item in self.inventory if item["stock"] <= item["reorder_threshold"]]
            low_stock_names = ", ".join([f"{item['name']} ({item['stock']})" for item in low_stock])
            resp = self._get_response_text("INVENTORY_CHECK", lang, items=low_stock_names)
            return {
                "intent": "INVENTORY_CHECK",
                "language": lang,
                "voice_response": resp,
                "low_stock_items": low_stock,
                "recommended_action": {
                    "type": "ONDC_PURCHASE",
                    "text": "1-Click Order 50 pkts Amul Milk (₹1,210)",
                    "sku": "AMUL-MILK-500",
                    "estimated_amount": 1210
                }
            }

        # Udhar intent
        elif any(w in q_lower for w in ["udhar", "khata", "due", "pending", "reminder", "sharma", "anil", "అప్పు", "బాకీ", "கடன்", "ಬಾಕಿ"]):
            total_due = sum(k["due_amount"] for k in self.khata)
            oldest = max(self.khata, key=lambda x: x["days_pending"])
            resp = self._get_response_text("KHATA_RECOVERY", lang, due=f"{total_due:,}", name=oldest["name"], cust_due=f"{oldest['due_amount']:,}", days=str(oldest["days_pending"]))
            return {
                "intent": "KHATA_RECOVERY",
                "language": lang,
                "voice_response": resp,
                "total_due": total_due,
                "top_defaulter": oldest,
                "recommended_action": {
                    "type": "SEND_WHATSAPP_REMINDER",
                    "text": f"Send 1-Click WhatsApp payment link to {oldest['name']}",
                    "target_customer": oldest["name"]
                }
            }

        # Loan intent
        elif any(w in q_lower for w in ["loan", "credit", "paisa", "working capital", "paise", "borrow", "రుణం", "கடன்", "ಸಾಲ"]):
            return self.evaluate_merchant_credit(lang)

        # General
        else:
            resp = self._get_response_text("GENERAL_ASSIST", lang)
            return {
                "intent": "GENERAL_ASSIST",
                "language": lang,
                "voice_response": resp,
                "soundbox_status": self.merchant_profile["soundbox_status"],
                "store_name": self.merchant_profile["store_name"]
            }

    # Generate Udhar reminder in specified language
    def generate_udhar_reminder(self, customer_id: str, language: str = "english") -> Dict[str, Any]:
        customer = next((k for k in self.khata if k["id"] == customer_id or k["name"].lower() in customer_id.lower()), None)
        if not customer:
            return {"error": "Customer not found in Khata ledger"}

        upi_link = f"upi://pay?pa={self.merchant_profile['upi_id']}&pn=Gupta%20Store&am={customer['due_amount']}&cu=INR&tn=Khata%20Bill%20Settlement"
        web_pay_link = f"https://paytm.me/pay/gupta-store?amt={customer['due_amount']}&cust={customer['id']}"

        lang = language.lower().strip()
        amt_str = f"₹{customer['due_amount']:,}"

        if lang == "telugu":
            msg = (
                f"నమస్కారం {customer['name']} గారు! 🙏\n\n"
                f"గుప్తా కిరాణా స్టోర్ నుండి శుభాకాంక్షలు. మీ పాత బకాయి "
                f"*{amt_str}* పెండింగ్‌లో ఉంది ({customer['notes']}).\n\n"
                f"ఎటువంటి శ్రమ లేకుండా పేటీఎం యూపీఐ ద్వారా చెల్లించడానికి ఇక్కడ నొక్కండి:\n"
                f"👉 {web_pay_link}\n\n"
                f"ధన్యవాదాలు! మీ రోజు శుభప్రదం కావాలి."
            )
        elif lang == "tamil":
            msg = (
                f"வணக்கம் {customer['name']} அவர்களே! 🙏\n\n"
                f"குப்தா மளிகைக் கடையின் வாழ்த்துகள். உங்கள் கடை பாக்கி "
                f"*{amt_str}* நிலுவையில் உள்ளது ({customer['notes']}).\n\n"
                f"பேடிஎம் யுபிஐ மூலம் உடனடியாக செலுத்த இங்கே கிளிக் செய்யவும்:\n"
                f"👉 {web_pay_link}\n\n"
                f"நன்றி! நல்நாளாக அமையட்டும்."
            )
        elif lang == "kannada":
            msg = (
                f"ನಮಸ್ಕಾರ {customer['name']} ಅವರೇ! 🙏\n\n"
                f"ಗುಪ್ತಾ ಕಿರಾಣಾ ಸ್ಟೋರ್‌ನಿಂದ ಶುಭಾಶಯಗಳು. ನಿಮ್ಮ ಹಳೆಯ ಬಾಕಿ ಮೊತ್ತ "
                f"*{amt_str}* ಬಾಕಿ ಉಳಿದಿದೆ ({customer['notes']}).\n\n"
                f"ಪೇಟಿಎಂ ಯುಪಿಐ ಮೂಲಕ 1-ಕ್ಲಿಕ್‌ನಲ್ಲಿ ಪಾವತಿಸಲು ಇಲ್ಲಿ ಒತ್ತಿ:\n"
                f"👉 {web_pay_link}\n\n"
                f"ಧನ್ಯವಾದಗಳು! ಶುಭ ದಿನ."
            )
        elif lang == "hindi":
            msg = (
                f"नमस्ते {customer['name']} जी! 🙏\n\n"
                f"गुप्ता किराना स्टोर की तरफ से शुभकामनाएं. आपका दुकान का पुराना बैलेंस "
                f"*{amt_str}* पेंडिंग है ({customer['notes']}).\n\n"
                f"बिना किसी झंझट के पेटीएम यूपीआई से 1-क्लिक में पे करने के लिए यहां टैप करें:\n"
                f"👉 {web_pay_link}\n\n"
                f"धन्यवाद! आपका दिन शुभ हो."
            )
        else: # English
            msg = (
                f"Hello {customer['name']}! 🙏\n\n"
                f"Greetings from Gupta Kirana Store. Your pending store balance is "
                f"*{amt_str}* ({customer['notes']}).\n\n"
                f"To settle conveniently in 1-click via Paytm UPI, please tap below:\n"
                f"👉 {web_pay_link}\n\n"
                f"Thank you for being a valued customer!"
            )

        customer["last_reminder"] = "Just now"

        return {
            "status": "SENT",
            "language": lang,
            "customer_name": customer["name"],
            "phone": customer["phone"],
            "due_amount": customer["due_amount"],
            "whatsapp_message": msg,
            "upi_deep_link": upi_link,
            "web_pay_link": web_pay_link,
            "sentiment": "POLITE_NEIGHBORHOOD_TONE"
        }

    # ONDC Restock
    def execute_ondc_restock(self, sku: str, quantity: int) -> Dict[str, Any]:
        item = next((i for i in self.inventory if i["sku"] == sku), None)
        distributor = next((d for d in self.ondc_distributors if d["sku"] == sku), self.ondc_distributors[0])

        if not item:
            return {"error": f"SKU {sku} not found"}

        total_cost = round(distributor["wholesale_price"] * quantity, 2)

        if self.merchant_profile["account_balance"] >= total_cost:
            self.merchant_profile["account_balance"] -= total_cost
            item["stock"] += quantity

            order_record = {
                "order_id": f"ONDC-PO-{datetime.datetime.now().strftime('%M%S')}",
                "item_name": item["name"],
                "quantity": quantity,
                "unit_wholesale_price": distributor["wholesale_price"],
                "total_amount": total_cost,
                "distributor": distributor["name"],
                "eta": distributor["delivery_eta"],
                "settlement": "Settled via Paytm Merchant Balance",
                "remaining_balance": round(self.merchant_profile["account_balance"], 2),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return {"status": "SUCCESS", "order": order_record}
        else:
            return {
                "status": "INSUFFICIENT_FUNDS",
                "message": "Account balance insufficient."
            }

    # Credit Underwriting
    def evaluate_merchant_credit(self, language: str = "english") -> Dict[str, Any]:
        max_eligible_limit = 250000
        resp = self._get_response_text("CREDIT_APPROVAL", language, limit=f"{max_eligible_limit:,}")

        return {
            "intent": "CREDIT_APPROVAL",
            "language": language,
            "pre_approved_amount": max_eligible_limit,
            "interest_rate_monthly": "1.15%",
            "daily_deduction_edi": 450,
            "disbursal_speed_seconds": 180,
            "underwriting_factors": {
                "daily_upi_velocity": "₹18,450/day",
                "soundbox_operational_days": "180+ consecutive days",
                "repeat_customer_frequency": "76.5%",
                "cashflow_stability_grade": "Tier A+ (Prime MSME)"
            },
            "voice_response": resp,
            "status": "READY_FOR_1CLICK_DISBURSAL"
        }
