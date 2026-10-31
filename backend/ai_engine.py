import os
import json
import re
from typing import Dict, Any, Tuple
from .mock_db import (
    STORE_PROFILE,
    TODAY_METRICS,
    INVENTORY_ITEMS,
    HOURLY_SALES,
    KHATA_LEDGER,
    LOAN_CREDIT_INSIGHTS,
    PAYTM_BUSINESS_UNIT_ECONOMICS
)

def detect_language(text: str) -> str:
    """Returns 'hi' if Hindi/Devanagari is detected or strong Hindi/Hinglish keywords, else 'en'."""
    hindi_keywords = [
        "bikri", "aaj", "kamaai", "stock", "khatam", "kitna", "banao", "bhejo",
        "kirana", "dukan", "samagri", "doodh", "bheed", "vyapar", "chhut", "paise",
        "kya", "kaise", "hai", "mujhe", "batao", "sunao", "chahiye", "udhar", "khata",
        "tagada", "ramesh", "bill", "parcha", "loan"
    ]
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return "hi"
    
    words = text.lower().split()
    if any(w in hindi_keywords for w in words):
        return "hi"
    return "en"

def process_merchant_query(query: str) -> Dict[str, Any]:
    """
    10/10 AI Engine: handles Sales, Stock, Khata/Udhaar ledger, Bill Scanning, 
    Lending Sanction, and WhatsApp Marketing.
    """
    q = query.lower().strip()
    lang = detect_language(query)

    # 1. KHATA & UDHAAR RECOVERY INTENT (The #1 Kirana Problem!)
    if any(k in q for k in ["khata", "udhar", "udhaar", "due", "pending", "ramesh", "tagada", "उधार", "खाता", "तगादा", "बाकी"]):
        total_due = sum(c["amount_due"] for c in KHATA_LEDGER)
        overdue_customers = [c for c in KHATA_LEDGER if c["status"] in ["overdue", "critical_overdue"]]

        if "ramesh" in q or "रमेश" in q:
            target = next((c for c in KHATA_LEDGER if "Ramesh" in c["name"]), KHATA_LEDGER[0])
            whatsapp_reminder = (
                f"नमस्ते {target['name']} जी! शर्मा सुपर स्टोर की ओर से विनम्र निवेदन। "
                f"आपका पिछला बिल ₹{target['amount_due']} ({target['last_items']}) पिछले {target['days_pending']} दिनों से बाकी है। "
                f"कृपया इस लिंक द्वारा पेटीएम यूपीआई से तुरंत भुगतान करें: https://p.paytm.me/pay?vpa=sharmastore@paytm&am={target['amount_due']}"
            )
            if lang == "hi":
                voice = (
                    f"रमेश वर्मा का ₹{target['amount_due']} का पुराना उधार {target['days_pending']} दिनों से बाकी है। "
                    f"सामान: {target['last_items']}। क्या मैं उन्हें पेटीएम यूपीआई पेमेंट लिंक के साथ व्हाट्सएप्प रिमाइंडर भेज दूँ?"
                )
                display = (
                    f"### 📒 रमेश वर्मा - खाता विवरण (Customer Credit Profile)\n\n"
                    f"- **ग्राहक:** {target['name']} ({target['phone']})\n"
                    f"- **बकाया राशि (Due):** 🔴 **₹{target['amount_due']}** ({target['days_pending']} दिनों से)\n"
                    f"- **अंतिम सामान:** {target['last_items']}\n\n"
                    f"**तैयार व्हाट्सएप पेमेंट रिमाइंडर:**\n"
                    f"```text\n{whatsapp_reminder}\n```\n"
                )
            else:
                voice = (
                    f"Ramesh Verma has a pending due of ₹{target['amount_due']} for {target['days_pending']} days for {target['last_items']}. "
                    f"Would you like me to send an automated WhatsApp payment link reminder?"
                )
                display = (
                    f"### 📒 Ramesh Verma - Digital Khata Profile\n\n"
                    f"- **Customer:** {target['name']} ({target['phone']})\n"
                    f"- **Outstanding Due:** 🔴 **₹{target['amount_due']}** ({target['days_pending']} days overdue)\n"
                    f"- **Purchased Items:** {target['last_items']}\n\n"
                    f"**Generated UPI Recovery Message:**\n"
                    f"```text\n{whatsapp_reminder}\n```\n"
                )

            return {
                "intent": "khata_single",
                "voice_text": voice,
                "display_text": display,
                "lang": lang,
                "action": {"type": "send_khata_reminder", "customer": target, "reminder_text": whatsapp_reminder}
            }

        # Overall Khata Summary
        if lang == "hi":
            voice = (
                f"राजेश जी, आपके खाते में कुल 4 ग्राहकों पर ₹{total_due:,} का उधार बाकी है। "
                f"इनमें से विकास माथुर पर ₹2,000 और अमित पटेल पर ₹950 का उधार 15 दिन से ज्यादा पुराना है। "
                f"मैंने सभी के लिए वन-क्लिक व्हाट्सएप पेमेंट तगादा तैयार कर दिया है।"
            )
            list_md = "\n".join([
                f"- **{c['name']}**: ₹{c['amount_due']} ({c['days_pending']} दिन) • *{c['last_items']}*"
                for c in KHATA_LEDGER
            ])
            display = (
                f"### 📒 डिजिटल खाता व उधार वसूली (Paytm Smart Khata)\n\n"
                f"- **कुल बकाया उधार (Total Credit Outstanding):** 🔴 **₹{total_due:,}**\n"
                f"- **अति-लंबित मामले (Critical Overdue):** 2 ग्राहक (15+ दिन)\n\n"
                f"{list_md}\n\n"
                f"👉 *नीचे 'सभी को तगादा भेजें' बटन दबाकर सीधे यूपीआई लिंक वाला मैसेज भेजें।*"
            )
        else:
            voice = (
                f"Mr. Rajesh, you have a total of ₹{total_due:,} pending across 4 customers. "
                f"Vikas Mathur (₹2,000) and Amit Patel (₹950) are overdue beyond 15 days. "
                f"I have prepared 1-click WhatsApp payment links for recovery."
            )
            list_md = "\n".join([
                f"- **{c['name']}**: ₹{c['amount_due']} ({c['days_pending']} days) • *{c['last_items']}*"
                for c in KHATA_LEDGER
            ])
            display = (
                f"### 📒 Paytm Smart Khata Ledger Overview\n\n"
                f"- **Total Outstanding Credit:** 🔴 **₹{total_due:,}**\n"
                f"- **Overdue Alerts:** 2 high-risk accounts (>15 days)\n\n"
                f"{list_md}\n\n"
                f"👉 *Click 'Broadcast UPI Reminders' to initiate automated collection.*"
            )

        return {
            "intent": "khata_summary",
            "voice_text": voice,
            "display_text": display,
            "lang": lang,
            "action": {"type": "show_khata_modal", "ledger": KHATA_LEDGER}
        }

    # 2. SALES & REVENUE INTENT
    if any(k in q for k in ["sale", "revenue", "bikri", "collection", "earning", "kamai", "aaj kitna", "today's total", "बिक्री", "कमाई", "कलेक्शन"]):
        if lang == "hi":
            voice = (
                f"राजेश जी, आज आपकी कुल बिक्री ₹{TODAY_METRICS['total_revenue']:,} हुई है। "
                f"इसमें से ₹{TODAY_METRICS['upi_revenue']:,} सीधे पेटीएम साउंडबॉक्स और यूपीआई से मिले हैं, "
                f"जो पिछले हफ्ते से अठारह प्रतिशत ज्यादा है!"
            )
            display = (
                f"### 📊 आज का व्यापार सारांश (Today's Business Summary)\n\n"
                f"- **कुल बिक्री (Total Revenue):** ₹{TODAY_METRICS['total_revenue']:,}\n"
                f"- **पेटीएम यूपीआई / साउंडबॉक्स:** ₹{TODAY_METRICS['upi_revenue']:,} ({TODAY_METRICS['soundbox_verified_txns']} पेमेंट्स)\n"
                f"- **कैश बिक्री (Cash):** ₹{TODAY_METRICS['cash_revenue']:,}\n"
                f"- **औसत बिल आकार (Avg Ticket):** ₹{TODAY_METRICS['avg_ticket_size']:.1f}\n"
                f"- **वृद्धि (Growth):** 🟢 **{TODAY_METRICS['comparison_vs_last_week']}** पिछले हफ्ते से बेहतर!\n\n"
                f"💡 *सलाह: शाम 7 बजे से 9 बजे के बीच सबसे ज्यादा ग्राहक आ रहे हैं। काउंटर पर तैयारी रखें।*"
            )
        else:
            voice = (
                f"Mr. Rajesh, your total revenue today is ₹{TODAY_METRICS['total_revenue']:,}. "
                f"Paytm UPI & Soundbox contributed ₹{TODAY_METRICS['upi_revenue']:,} across {TODAY_METRICS['soundbox_verified_txns']} transactions, "
                f"up 18.4% compared to last week!"
            )
            display = (
                f"### 📊 Today's Sales & Collection Overview\n\n"
                f"- **Total Revenue:** ₹{TODAY_METRICS['total_revenue']:,}\n"
                f"- **Paytm UPI / Soundbox:** ₹{TODAY_METRICS['upi_revenue']:,} ({TODAY_METRICS['soundbox_verified_txns']} txns)\n"
                f"- **Cash Receipts:** ₹{TODAY_METRICS['cash_revenue']:,}\n"
                f"- **Average Bill Size:** ₹{TODAY_METRICS['avg_ticket_size']:.1f}\n"
                f"- **Growth vs Last Week:** 🟢 **{TODAY_METRICS['comparison_vs_last_week']}**\n\n"
                f"💡 *AI Copilot Insight: Peak sales occurred between 7:00 PM – 9:00 PM. High demand in Dairy & Cooking Essentials.*"
            )

        return {
            "intent": "sales_summary",
            "voice_text": voice,
            "display_text": display,
            "lang": lang,
            "action": {"type": "highlight_sales", "metric": TODAY_METRICS}
        }

    # 3. INVENTORY & STOCK ALERT INTENT
    if any(k in q for k in ["stock", "inventory", "khatam", "saman", "reorder", "milk", "oil", "maggi", "आइटम", "स्टॉक", "सामान"]):
        critical_items = [i for i in INVENTORY_ITEMS if i["status"] in ["critical_low", "low"]]
        
        if lang == "hi":
            voice = (
                f"सावधान! अमूल ताज़ा दूध के सिर्फ 4 पैकेट और फॉर्च्यून सरसों तेल की केवल 3 बोतलें बची हैं। "
                f"मैगी नूडल्स भी खत्म होने वाली है। क्या मैं डिस्ट्रीब्यूटर को री-ऑर्डर का संदेश भेज दूँ?"
            )
            item_list_md = "\n".join([
                f"- ⚠️ **{item['name_hi']}**: वर्तमान स्टॉक **{item['current_stock']} {item['unit']}** (सुरक्षित सीमा: {item['reorder_threshold']})"
                for item in critical_items
            ])
            display = (
                f"### 📦 तत्काल स्टॉक री-ऑर्डर चेतावनी (Low Stock Radar)\n\n"
                f"{item_list_md}\n\n"
                f"**सुझाया गया री-ऑर्डर आर्डर (1-क्लिक डिस्ट्रीब्यूटर PO):**\n"
                f"1. अमूल ताज़ा दूध: 30 पैकेट्स\n"
                f"2. फॉर्च्यून सरसों तेल (1L): 2 कार्टन (24 बोतलें)\n"
                f"3. मैगी 2-मिनट (70g): 50 पैकेट्स\n\n"
                f"👉 *'री-ऑर्डर PO भेजें' बटन दबाकर सीधे थोक डीलर को व्हाट्सएप आर्डर भेजा जा सकता है।*"
            )
        else:
            voice = (
                f"Warning! Amul Milk has only 4 packets remaining, and Fortune Mustard Oil has only 3 bottles left. "
                f"Maggi Noodles is also running low. Would you like me to trigger an automated distributor restock order?"
            )
            item_list_md = "\n".join([
                f"- ⚠️ **{item['name']}**: Only **{item['current_stock']} {item['unit']}** left (Alert limit: {item['reorder_threshold']})"
                for item in critical_items
            ])
            display = (
                f"### 📦 Critical Stock Reorder Alerts\n\n"
                f"{item_list_md}\n\n"
                f"**AI Suggested Restock Purchase Order:**\n"
                f"1. Amul Taaza Milk (500ml): 30 packets\n"
                f"2. Fortune Mustard Oil (1L): 2 Cartons (24 bottles)\n"
                f"3. Maggi 2-Minute Noodles: 50 packets\n\n"
                f"👉 *Click 'Dispatch PO to Supplier' to send one-tap order via WhatsApp.*"
            )

        return {
            "intent": "inventory_alert",
            "voice_text": voice,
            "display_text": display,
            "lang": lang,
            "action": {"type": "reorder_draft", "items": critical_items}
        }

    # 4. WHATSAPP MARKETING & FESTIVE PROMO INTENT
    if any(k in q for k in ["promo", "marketing", "whatsapp", "diwali", "offer", "discount", "chhut", "message", "प्रमोशन", "व्हाट्सएप", "छूट", "ऑफर"]):
        if lang == "hi":
            promo_msg = (
                f"🎉 *शर्मा सुपर स्टोर - विशेष ग्राहक ऑफर!* 🎉\n\n"
                f"नमस्ते! हमारे सम्मानित ग्राहकों के लिए खास छूट:\n"
                f"✅ ₹999 से अधिक की खरीदारी पर फ्लैट 10% की छूट!\n"
                f"✅ फॉर्च्यून तेल व ड्राई फ्रूट्स पर विशेष बचत!\n"
                f"📲 पेटीएम यूपीआई द्वारा आसान और सुरक्षित भुगतान।\n\n"
                f"📍 शर्मा सुपर स्टोर, सेक्टर 18, नोएडा\n"
                f"📞 होम डिलीवरी के लिए तुरंत रिप्लाई करें!"
            )
            voice = (
                "राजेश जी, मैंने आपके ग्राहकों के लिए 10% छूट वाला आकर्षक व्हाट्सएप प्रमोशन संदेश तैयार कर दिया है। "
                "आप इसे एक क्लिक में अपने नियमित ग्राहकों को भेज सकते हैं।"
            )
            display = (
                f"### 📢 1-क्लिक व्हाट्सएप प्रमोशन जनरेटर (Customer Campaign)\n\n"
                f"```text\n{promo_msg}\n```\n\n"
                f"🎯 **टारगेट ऑडियंस:** पिछले 30 दिनों में पेटीएम साउंडबॉक्स से भुगतान करने वाले 320 ग्राहक।\n"
                f"📈 **अनुमानित अतिरिक्त बिक्री:** +₹12,000 सप्ताहांत में।"
            )
        else:
            promo_msg = (
                f"🎉 *Sharma Super Store - Special Weekend Deal!* 🎉\n\n"
                f"Dear Customer,\n"
                f"Enjoy exclusive savings on your daily groceries:\n"
                f"✅ Flat 10% OFF on all bills above ₹999!\n"
                f"✅ Special discounts on Cooking Essentials & Snacks!\n"
                f"📲 Pay seamlessly using Paytm UPI / Soundbox.\n\n"
                f"📍 Sharma Super Store, Sector 18, Noida\n"
                f"📞 Call/WhatsApp for Free Home Delivery!"
            )
            voice = (
                "Mr. Rajesh, I have generated a customized 10% weekend discount campaign for WhatsApp. "
                "You can broadcast it to your regular customers with one click."
            )
            display = (
                f"### 📢 1-Click Hyperlocal WhatsApp Campaign\n\n"
                f"```text\n{promo_msg}\n```\n\n"
                f"🎯 **Target Reach:** 320 loyal shoppers based on recent Paytm transactions.\n"
                f"📈 **Expected Impact:** +15% basket size increase this weekend."
            )

        return {
            "intent": "whatsapp_campaign",
            "voice_text": voice,
            "display_text": display,
            "lang": lang,
            "action": {"type": "whatsapp_share", "text": promo_msg}
        }

    # 5. LOAN & CREDITWORTHINESS INTENT
    if any(k in q for k in ["loan", "credit", "udhar", "paisa chahiye", "eligible", "patrata", "लोन", "उधार", "पात्रता", "कर्ज"]):
        if lang == "hi":
            voice = (
                f"बधाई हो राजेश जी! आपके नियमित पेटीएम यूपीआई और साउंडबॉक्स लेनदेन के आधार पर "
                f"आप ₹2,50,000 के प्री-एप्रूव्ड मर्चेंट लोन के लिए पात्र हैं। "
                f"कोई कागजी कार्रवाई नहीं है, और दैनिक भुगतान केवल ₹320 साउंडबॉक्स सेटलमेंट से कटेगा।"
            )
            display = (
                f"### 💰 पेटीएम मर्चेंट ग्रोथ लोन (Pre-Approved Credit Partner)\n\n"
                f"- **स्वीकृत राशि (Eligible Amount):** 🟢 **₹{LOAN_CREDIT_INSIGHTS['pre_approved_amount']:,}**\n"
                f"- **ब्याज दर (Interest Rate):** {LOAN_CREDIT_INSIGHTS['interest_rate']}\n"
                f"- **दैनिक ईएमआई (Daily Auto-Deduction):** {LOAN_CREDIT_INSIGHTS['daily_deduction_via_soundbox']}\n"
                f"- **अवधि (Tenure):** {LOAN_CREDIT_INSIGHTS['tenure_months']} महीने\n"
                f"- **क्रेडिट हेल्थ (Credit Health):** {LOAN_CREDIT_INSIGHTS['credit_score_indicator']}\n\n"
                f"✅ *शून्य कागजात! 2 मिनट में सीधे आपके बैंक खाते में रकम जमा होगी।*"
            )
        else:
            voice = (
                f"Great news, Mr. Rajesh! Based on your consistent Paytm UPI collections, "
                f"you are pre-approved for a ₹2,50,000 instant merchant growth loan at 1.15% monthly interest. "
                f"Zero paperwork is required, with an easy auto-deduction of ₹320 per day."
            )
            display = (
                f"### 💰 Paytm Merchant Growth Loan (Pre-Approved Credit)\n\n"
                f"- **Pre-Approved Limit:** 🟢 **₹{LOAN_CREDIT_INSIGHTS['pre_approved_amount']:,}**\n"
                f"- **Monthly Interest:** {LOAN_CREDIT_INSIGHTS['interest_rate']}\n"
                f"- **Daily Soundbox Repayment:** {LOAN_CREDIT_INSIGHTS['daily_deduction_via_soundbox']}\n"
                f"- **Repayment Period:** {LOAN_CREDIT_INSIGHTS['tenure_months']} Months\n"
                f"- **Eligibility Rating:** {LOAN_CREDIT_INSIGHTS['credit_score_indicator']}\n\n"
                f"✅ *Instant disbursement into your linked bank account within 2 minutes.*"
            )

        return {
            "intent": "merchant_loan",
            "voice_text": voice,
            "display_text": display,
            "lang": lang,
            "action": {"type": "apply_loan", "details": LOAN_CREDIT_INSIGHTS}
        }

    # 6. SCAN BILL / PARCHA INTENT (Visual AI)
    if any(k in q for k in ["bill", "parcha", "invoice", "scan", "बिल", "पर्चा", "स्कैन"]):
        if lang == "hi":
            voice = (
                "राजेश जी, आप अपने थोक डिस्ट्रीब्यूटर के पर्चे या बिल की फोटो अपलोड करें। "
                "एआई अपने आप सामान और रेट पढ़कर आपकी इन्वेंटरी को अपडेट कर देगा।"
            )
            display = (
                f"### 📷 विज़ुअल बिल / पर्चा स्कैनर (Smart Invoice OCR)\n\n"
                f"थोक व्यापारी का हस्तलिखित पर्चा या प्रिंटेड इनवॉइस स्कैन करें:\n"
                f"- 🛒 **ऑटो-आइटम डिटेक्शन:** आटा, तेल, दाल, बिस्कुट\n"
                f"- 💵 **लागत मूल्य व मार्जिन गणना:** अपने आप खरीद भाव अपडेट होगा\n"
                f"- 📦 **1-टैप इन्वेंटरी स्टॉक-इन:** बिना कंप्यूटर में टाइप किए स्टॉक बढ़ जाएगा\n\n"
                f"👉 *नीचे 'बिल फोटो स्कैन करें' बटन पर क्लिक करके सैंपल पर्चा टेस्ट करें।*"
            )
        else:
            voice = (
                "Mr. Rajesh, upload or snap a photo of your distributor's wholesale invoice or paper slip. "
                "AI will extract all line items, calculate margins, and update your stock automatically."
            )
            display = (
                f"### 📷 Visual Wholesale Invoice Scanner (Smart OCR)\n\n"
                f"Scan handwritten distributor parchas or printed tax invoices:\n"
                f"- 🛒 **Auto Item Recognition:** Identifies brands, sizes, and quantities\n"
                f"- 💵 **Cost & Margin Calc:** Automatically calculates cost per unit\n"
                f"- 📦 **1-Tap Inventory Stock-in:** Eliminates manual data entry\n\n"
                f"👉 *Click 'Scan Wholesale Bill' below to try the sample invoice parser.*"
            )

        return {
            "intent": "scan_bill",
            "voice_text": voice,
            "display_text": display,
            "lang": lang,
            "action": {"type": "open_bill_scanner"}
        }

    # 7. PEAK HOUR / TRAFFIC INTENT
    if any(k in q for k in ["rush", "bheed", "peak", "crowd", "samay", "time", "भीड़", "समय", "ग्राहक"]):
        if lang == "hi":
            voice = (
                "राजेश जी, आपके स्टोर पर सबसे ज्यादा भीड़ शाम 7 बजे से रात 9 बजे के बीच होती है। "
                "इस समय कुल दैनिक बिक्री का 38% हिस्सा आता है। मेरा सुझाव है कि शाम 6:30 बजे ही चेंज और पैकिंग तैयार रखें।"
            )
            display = (
                f"### ⏰ पीक आवर विश्लेषण (Store Traffic Pattern)\n\n"
                f"- 🕒 **मुख्य भीड़ का समय:** **शाम 7:00 PM – 9:00 PM**\n"
                f"- 🛒 **उच्चतम बिक्री स्लॉट:** 8:00 PM (40 ट्रांजेक्शन, ₹8,800 बिक्री)\n"
                f"- ⚡ **सिफारिशें:**\n"
                f"  1. शाम 6:30 बजे दूध और ब्रेड का अतिरिक्त स्टॉक काउंटर पर रखें।\n"
                f"  2. साउंडबॉक्स की बैटरी व आवाज़ की जाँच कर लें।\n"
                f"  3. काउंटर पर 2 लोगों की उपस्थिति रखें ताकि कतार न लगे।"
            )
        else:
            voice = (
                "Mr. Rajesh, your peak customer footfall happens between 7:00 PM and 9:00 PM, "
                "which accounts for 38% of your entire day's revenue. We recommend prepping dairy and snacks by 6:30 PM."
            )
            display = (
                f"### ⏰ Footfall & Peak Hour Analysis\n\n"
                f"- 🕒 **Peak Shopping Window:** **7:00 PM – 9:00 PM**\n"
                f"- 🛒 **Busiest Hour:** 8:00 PM (40 customer checkouts, ₹8,800 revenue)\n"
                f"- ⚡ **AI Action Plan:**\n"
                f"  1. Pre-bundle high velocity snacks and staple combos.\n"
                f"  2. Ensure Paytm Soundbox volume is clear for quick customer audio confirmations.\n"
                f"  3. Maintain change for cash customers to prevent queues."
            )

        return {
            "intent": "peak_hours",
            "voice_text": voice,
            "display_text": display,
            "lang": lang,
            "action": {"type": "show_traffic_chart", "hourly": HOURLY_SALES}
        }

    # DEFAULT GREETING
    if lang == "hi":
        voice = (
            "नमस्ते राजेश जी! मैं आपका पेटीएम व्यापार साथी हूँ। "
            "आप मुझसे आज की बिक्री, खाता-उधार, खत्म होने वाले सामान या लोन के बारे में कभी भी पूछ सकते हैं।"
        )
        display = (
            f"### 🤖 नमस्ते Rajesh Ji, मैं हूँ आपका पेटीएम व्यापार AI!\n\n"
            f"मैं आपके स्टोर के डेटा और पेटीएम साउंडबॉक्स 3.0 से जुड़ा हुआ हूँ। आप मुझसे बोलकर पूछ सकते हैं:\n\n"
            f"- 🎙️ *\"आज की कुल बिक्री कितनी हुई?\"*\n"
            f"- 🎙️ *\"रमेश का कितना उधार बाकी है?\"*\n"
            f"- 🎙️ *\"कौन सा सामान खत्म होने वाला है?\"*\n"
            f"- 🎙️ *\"दीवाली का व्हाट्सएप डिस्काउंट मैसेज बनाओ\"*\n"
            f"- 🎙️ *\"थोक डीलर का बिल स्कैन करो\"*\n"
            f"- 🎙️ *\"मर्चेंट लोन की पात्रता चेक करो\"*"
        )
    else:
        voice = (
            "Hello Mr. Rajesh! I am your Paytm Vyapar AI Business Partner. "
            "Ask me about your daily revenue, customer khata dues, depleted stock, or instant business loans."
        )
        display = (
            f"### 🤖 Welcome to Paytm Vyapar AI Co-pilot!\n\n"
            f"Connected to **Sharma Super Store** (Soundbox 3.0: SBOX-IND-4091).\n\n"
            f"Try asking with your voice:\n"
            f"- 🎙️ *\"What are today's sales and top collections?\"*\n"
            f"- 🎙️ *\"How much pending khata does Ramesh owe?\"*\n"
            f"- 🎙️ *\"Which inventory items need restock?\"*\n"
            f"- 🎙️ *\"Create a WhatsApp weekend discount campaign\"*\n"
            f"- 🎙️ *\"Scan wholesale invoice bill\"*\n"
            f"- 🎙️ *\"Check my merchant loan limit\"*"
        )

    return {
        "intent": "general_greeting",
        "voice_text": voice,
        "display_text": display,
        "lang": lang,
        "action": {"type": "general"}
    }
