import os
import json
from typing import Dict, Any, List

class MerchantCopilotEngine:
    """
    Autonomous Multi-Agent Copilot Engine for Paytm Soundbox & Merchants.
    Supports Multi-Business Profiles: Kirana, Pharmacy, Cafe/Restaurant, Apparel, Electronics.
    Supports 5 Indic Languages: English, Telugu, Hindi, Tamil, Kannada.
    """

    BUSINESS_PROFILES = {
        "kirana": {
            "name": "Kirana & Grocery",
            "merchant_profile": {
                "store_name": "Sri Lakshmi Provision & Kirana Store",
                "owner": "Ramesh Gupta",
                "location": "Koramangala 4th Block, Bengaluru (Pin: 560034)",
                "upi_id": "guptakirana@paytm",
                "soundbox_id": "SB-4.0-BLR-89211",
                "soundbox_status": "ONLINE (Dual-Mic Active)",
                "account_balance": 48250.00,
                "today_collection": 18420.00,
                "today_txns": 64,
                "top_item": "Amul Taaza Milk 500ml",
                "credit_limit": 250000.00
            },
            "inventory": [
                {"sku": "AMUL-MILK-500", "name": "Amul Taaza Milk 500ml", "category": "Dairy", "stock": 4, "reorder_threshold": 15, "cost_price": 24.5, "mrp": 27.0, "daily_velocity": 38, "status": "CRITICAL"},
                {"sku": "THUMS-750", "name": "Thums Up 750ml", "category": "Beverages", "stock": 8, "reorder_threshold": 20, "cost_price": 36.0, "mrp": 45.0, "daily_velocity": 24, "status": "LOW"},
                {"sku": "AMUL-BTR-100", "name": "Amul Butter 100g", "category": "Dairy", "stock": 6, "reorder_threshold": 12, "cost_price": 51.0, "mrp": 58.0, "daily_velocity": 14, "status": "LOW"},
                {"sku": "TATA-TEA-250", "name": "Tata Tea Gold 250g", "category": "Beverages", "stock": 25, "reorder_threshold": 10, "cost_price": 135.0, "mrp": 160.0, "daily_velocity": 6, "status": "HEALTHY"}
            ],
            "khata": [
                {"id": "K1", "name": "Anil Verma Gym", "phone": "+91 98450 99887", "due_amount": 4850, "days_pending": 18, "last_reminder": "5 days ago", "notes": "Eggs crate & Oats", "risk": "High"},
                {"id": "K2", "name": "Ramesh Sharma", "phone": "+91 98765 43210", "due_amount": 3420, "days_pending": 12, "last_reminder": "2 days ago", "notes": "Atta 10kg & Oil", "risk": "Moderate"},
                {"id": "K3", "name": "Sita Ram Tailor", "phone": "+91 98111 22334", "due_amount": 1180, "days_pending": 5, "last_reminder": "Never", "notes": "Tea & Sugar", "risk": "Low"}
            ],
            "hyperlocal_trends": [
                {"trend": "Cold Drinks & Hydration Surge", "change": "+44%", "type": "SURGE", "reason": "Heatwave trigger: Temperatures +3.5°C above normal.", "action": "Increase stock buffer by 30 units."},
                {"trend": "Pooja Ghee & Flowers", "change": "+32%", "type": "UPCOMING", "reason": "Weekend temple rush in 4th block.", "action": "Pre-order 20 packets from regional distributor."},
                {"trend": "Brand X Nachos Stagnant", "change": "-60%", "type": "DEAD_STOCK", "reason": "Zero movement in 14 days.", "action": "Bundle with cold drinks at 10% discount."}
            ],
            "ondc_distributors": [
                {"name": "Sri Balaji Dairy Agency", "distance_km": 1.2, "sku": "Amul Taaza Milk 500ml", "stock": "4 pkts (Critical)", "wholesale_price": 24.2, "mrp": 27.0, "action": "Reorder (50 pkts)", "qty": 50, "amt": "₹1,210"},
                {"name": "Metro Cash & Carry ONDC", "distance_km": 3.8, "sku": "Thums Up 750ml", "stock": "8 bottles (Low)", "wholesale_price": 35.5, "mrp": 45.0, "action": "Reorder (24 bots)", "qty": 24, "amt": "₹852"},
                {"name": "Karnataka Dairy Federation ONDC", "distance_km": 2.1, "sku": "Amul Butter 100g", "stock": "6 pkts (Low)", "wholesale_price": 50.5, "mrp": 58.0, "action": "Reorder (20 pkts)", "qty": 20, "amt": "₹1,010"}
            ]
        },
        "pharmacy": {
            "name": "Pharmacy & Medical",
            "merchant_profile": {
                "store_name": "Sanjivani MedPlus Pharmacy & Wellness",
                "owner": "Dr. Pradeep Rao",
                "location": "Jayanagar 4th T Block, Bengaluru (Pin: 560041)",
                "upi_id": "sanjivanipharma@paytm",
                "soundbox_id": "SB-4.0-BLR-90412",
                "soundbox_status": "ONLINE (Dual-Mic Active)",
                "account_balance": 68400.00,
                "today_collection": 24850.00,
                "today_txns": 88,
                "top_item": "Dolo 650mg Tablets Strip",
                "credit_limit": 350000.00
            },
            "inventory": [
                {"sku": "DOLO-650", "name": "Dolo 650mg Tablets Strip", "category": "Analgesic", "stock": 5, "reorder_threshold": 25, "cost_price": 26.0, "mrp": 34.0, "daily_velocity": 42, "status": "CRITICAL"},
                {"sku": "AZI-500", "name": "Azithromycin 500mg Strip", "category": "Antibiotic", "stock": 7, "reorder_threshold": 18, "cost_price": 68.0, "mrp": 89.0, "daily_velocity": 16, "status": "LOW"},
                {"sku": "BENADRYL-100", "name": "Benadryl Cough Syrup 100ml", "category": "Cough & Cold", "stock": 8, "reorder_threshold": 15, "cost_price": 92.0, "mrp": 120.0, "daily_velocity": 12, "status": "LOW"},
                {"sku": "ORS-ELECT", "name": "Electral ORS Powder 21g", "category": "Hydration", "stock": 45, "reorder_threshold": 20, "cost_price": 16.5, "mrp": 22.0, "daily_velocity": 18, "status": "HEALTHY"}
            ],
            "khata": [
                {"id": "KP1", "name": "Dr. Mehra Clinic", "phone": "+91 98451 11223", "due_amount": 6800, "days_pending": 15, "last_reminder": "3 days ago", "notes": "Syringes, Dettol & Gloves bulk", "risk": "Moderate"},
                {"id": "KP2", "name": "Anil Verma Gym", "phone": "+91 98450 99887", "due_amount": 3200, "days_pending": 10, "last_reminder": "4 days ago", "notes": "Protein shakers & Multivitamins", "risk": "Moderate"},
                {"id": "KP3", "name": "Mrs. Revathi Senior Citizen", "phone": "+91 99112 33445", "due_amount": 1450, "days_pending": 6, "last_reminder": "Never", "notes": "Monthly BP & Diabetes medicines", "risk": "Low"}
            ],
            "hyperlocal_trends": [
                {"trend": "Seasonal Flu & Paracetamol Surge", "change": "+58%", "type": "SURGE", "reason": "Viral fever breakout in surrounding 2km wards.", "action": "Stock up 100 strips of Dolo 650 via ONDC."},
                {"trend": "ORS & Dehydration Electrolytes", "change": "+36%", "type": "SURGE", "reason": "Humid afternoons driving clinic prescriptions.", "action": "Pre-order 50 sachets of Electral."},
                {"trend": "Slow Moving Antacid Brands", "change": "-45%", "type": "DEAD_STOCK", "reason": "Brand Z Gel has zero sales in 20 days.", "action": "Return batch to supplier for credit note."}
            ],
            "ondc_distributors": [
                {"name": "Karnataka Medico Wholesale ONDC", "distance_km": 2.4, "sku": "Dolo 650mg Tablets Strip", "stock": "5 strips (Critical)", "wholesale_price": 25.5, "mrp": 34.0, "action": "Reorder (50 strips)", "qty": 50, "amt": "₹1,275"},
                {"name": "Cipla Direct B2B Distributor", "distance_km": 4.1, "sku": "Azithromycin 500mg Strip", "stock": "7 strips (Low)", "wholesale_price": 67.0, "mrp": 89.0, "action": "Reorder (20 strips)", "qty": 20, "amt": "₹1,340"},
                {"name": "Apollo Supply Chain ONDC", "distance_km": 3.0, "sku": "Benadryl Cough Syrup 100ml", "stock": "8 bottles (Low)", "wholesale_price": 90.0, "mrp": 120.0, "action": "Reorder (25 bottles)", "qty": 25, "amt": "₹2,250"}
            ]
        },
        "restaurant": {
            "name": "Cafe & Restaurant",
            "merchant_profile": {
                "store_name": "Udupi Grand Cafe & Tiffin Express",
                "owner": "Shankar Narayana",
                "location": "Indiranagar 100ft Road, Bengaluru (Pin: 560038)",
                "upi_id": "udupigrand@paytm",
                "soundbox_id": "SB-4.0-BLR-91033",
                "soundbox_status": "ONLINE (Dual-Mic Active)",
                "account_balance": 82100.00,
                "today_collection": 32600.00,
                "today_txns": 142,
                "top_item": "Special Filter Coffee",
                "credit_limit": 400000.00
            },
            "inventory": [
                {"sku": "NANDINI-MILK", "name": "Nandini Full Cream Milk 1L", "category": "Dairy", "stock": 6, "reorder_threshold": 30, "cost_price": 48.0, "mrp": 54.0, "daily_velocity": 85, "status": "CRITICAL"},
                {"sku": "COFFEE-DECOCT", "name": "Chikmagalur Roast Coffee 1kg", "category": "Beverages", "stock": 3, "reorder_threshold": 10, "cost_price": 420.0, "mrp": 550.0, "daily_velocity": 5, "status": "LOW"},
                {"sku": "IDLI-RICE-25", "name": "Idli Boiled Rice 25kg Bag", "category": "Grains", "stock": 2, "reorder_threshold": 5, "cost_price": 950.0, "mrp": 1200.0, "daily_velocity": 1.5, "status": "LOW"},
                {"sku": "SAMBAR-MASALA", "name": "Udupi Sambar Powder 5kg", "category": "Spices", "stock": 8, "reorder_threshold": 4, "cost_price": 750.0, "mrp": 950.0, "daily_velocity": 1, "status": "HEALTHY"}
            ],
            "khata": [
                {"id": "KR1", "name": "Tech Corp Office Tiffin", "phone": "+91 98452 77889", "due_amount": 7800, "days_pending": 14, "last_reminder": "3 days ago", "notes": "Monthly team breakfast meals", "risk": "Moderate"},
                {"id": "KR2", "name": "Anil Verma Gym", "phone": "+91 98450 99887", "due_amount": 2850, "days_pending": 8, "last_reminder": "2 days ago", "notes": "Daily egg omelettes & juice", "risk": "Low"},
                {"id": "KR3", "name": "City Cab Drivers Association", "phone": "+91 98888 12345", "due_amount": 1650, "days_pending": 6, "last_reminder": "Never", "notes": "Night shift tea & buns", "risk": "Low"}
            ],
            "hyperlocal_trends": [
                {"trend": "Evening Office Coffee Rush", "change": "+52%", "type": "SURGE", "reason": "Office staff return driving 4 PM - 7 PM tea peak.", "action": "Buffer 40 litres of Nandini milk before 3:30 PM."},
                {"trend": "Ghee Roast & Dosa Popularity", "change": "+34%", "type": "SURGE", "reason": "Weekend food delivery surges on Swiggy/Zomato.", "action": "Ensure 15kg idli batter prepared in advance."},
                {"trend": "Packaged Soda Low Margin", "change": "-25%", "type": "DEAD_STOCK", "reason": "Customers preferring fresh buttermilk & nimbu pani.", "action": "Promote house buttermilk over bottled soda."}
            ],
            "ondc_distributors": [
                {"name": "Karnataka Dairy KMF ONDC", "distance_km": 1.5, "sku": "Nandini Full Cream Milk 1L", "stock": "6 pkts (Critical)", "wholesale_price": 47.5, "mrp": 54.0, "action": "Reorder (40 pkts)", "qty": 40, "amt": "₹1,900"},
                {"name": "Chikmagalur Planters B2B ONDC", "distance_km": 4.5, "sku": "Chikmagalur Roast Coffee 1kg", "stock": "3 bags (Low)", "wholesale_price": 410.0, "mrp": 550.0, "action": "Reorder (10 bags)", "qty": 10, "amt": "₹4,100"},
                {"name": "Bangalore Rice Traders ONDC", "distance_km": 3.2, "sku": "Idli Boiled Rice 25kg Bag", "stock": "2 bags (Low)", "wholesale_price": 930.0, "mrp": 1200.0, "action": "Reorder (5 bags)", "qty": 5, "amt": "₹4,650"}
            ]
        },
        "apparel": {
            "name": "Garments & Apparel",
            "merchant_profile": {
                "store_name": "Trends Fashion & Readymade Garments",
                "owner": "Vikram Sethi",
                "location": "Commercial Street, Bengaluru (Pin: 560001)",
                "upi_id": "trendsfashion@paytm",
                "soundbox_id": "SB-4.0-BLR-92341",
                "soundbox_status": "ONLINE (Dual-Mic Active)",
                "account_balance": 95400.00,
                "today_collection": 42500.00,
                "today_txns": 36,
                "top_item": "Rayon Printed Kurti (M/L)",
                "credit_limit": 500000.00
            },
            "inventory": [
                {"sku": "KURTI-RAYON-M", "name": "Rayon Printed Kurti (Medium)", "category": "Ethnic Wear", "stock": 3, "reorder_threshold": 15, "cost_price": 320.0, "mrp": 599.0, "daily_velocity": 18, "status": "CRITICAL"},
                {"sku": "DENIM-SLIM-32", "name": "Men Slim Fit Denim 32", "category": "Western Wear", "stock": 5, "reorder_threshold": 12, "cost_price": 480.0, "mrp": 899.0, "daily_velocity": 8, "status": "LOW"},
                {"sku": "COTTON-SHIRT-L", "name": "Casual Cotton Shirt Large", "category": "Menswear", "stock": 6, "reorder_threshold": 10, "cost_price": 280.0, "mrp": 499.0, "daily_velocity": 7, "status": "LOW"},
                {"sku": "SILK-DUPATTA", "name": "Banarasi Silk Dupatta", "category": "Accessories", "stock": 25, "reorder_threshold": 8, "cost_price": 180.0, "mrp": 350.0, "daily_velocity": 4, "status": "HEALTHY"}
            ],
            "khata": [
                {"id": "KA1", "name": "Geeta Boutique", "phone": "+91 98453 44556", "due_amount": 9200, "days_pending": 20, "last_reminder": "4 days ago", "notes": "Festive designer kurtis bulk", "risk": "High"},
                {"id": "KA2", "name": "Anil Verma Gym", "phone": "+91 98450 99887", "due_amount": 3500, "days_pending": 9, "last_reminder": "3 days ago", "notes": "Gym track pants & tees", "risk": "Low"},
                {"id": "KA3", "name": "Rajesh Tailors", "phone": "+91 99114 55667", "due_amount": 2100, "days_pending": 7, "last_reminder": "Never", "notes": "Suiting fabrics & lining", "risk": "Low"}
            ],
            "hyperlocal_trends": [
                {"trend": "Festive Ethnic Kurti Surge", "change": "+64%", "type": "SURGE", "reason": "Upcoming wedding & festival season shopping.", "action": "Stock 50 units of fast-selling Kurtis via ONDC."},
                {"trend": "Cotton Summer Casuals", "change": "+38%", "type": "SURGE", "reason": "Warm weather driving breathable apparel demand.", "action": "Increase pastel shirt inventory buffer."},
                {"trend": "Heavy Winter Jackets Dead Stock", "change": "-70%", "type": "DEAD_STOCK", "reason": "Unseasonal warmth stopping outerwear sales.", "action": "Clearance sale at 30% discount to unlock capital."}
            ],
            "ondc_distributors": [
                {"name": "Surat Textile Hub on ONDC", "distance_km": 5.2, "sku": "Rayon Printed Kurti (Medium)", "stock": "3 pcs (Critical)", "wholesale_price": 310.0, "mrp": 599.0, "action": "Reorder (30 pcs)", "qty": 30, "amt": "₹9,300"},
                {"name": "Tirupur Knitwear B2B ONDC", "distance_km": 6.8, "sku": "Casual Cotton Shirt Large", "stock": "6 pcs (Low)", "wholesale_price": 270.0, "mrp": 499.0, "action": "Reorder (20 pcs)", "qty": 20, "amt": "₹5,400"},
                {"name": "Bellary Denim Factory ONDC", "distance_km": 4.9, "sku": "Men Slim Fit Denim 32", "stock": "5 pcs (Low)", "wholesale_price": 465.0, "mrp": 899.0, "action": "Reorder (15 pcs)", "qty": 15, "amt": "₹6,975"}
            ]
        },
        "electronics": {
            "name": "Mobile & Electronics",
            "merchant_profile": {
                "store_name": "Digital Hub Mobile & Repair Center",
                "owner": "Mohammed Imran",
                "location": "SP Road Electronics Market, Bengaluru (Pin: 560002)",
                "upi_id": "digitalhub@paytm",
                "soundbox_id": "SB-4.0-BLR-93882",
                "soundbox_status": "ONLINE (Dual-Mic Active)",
                "account_balance": 54200.00,
                "today_collection": 21300.00,
                "today_txns": 45,
                "top_item": "20W Type-C Fast Charger",
                "credit_limit": 300000.00
            },
            "inventory": [
                {"sku": "CHG-20W-PD", "name": "20W Type-C Fast Charger", "category": "Accessories", "stock": 4, "reorder_threshold": 15, "cost_price": 140.0, "mrp": 299.0, "daily_velocity": 16, "status": "CRITICAL"},
                {"sku": "GLASS-9D-UNIV", "name": "9D Tempered Glass Protector", "category": "Protection", "stock": 9, "reorder_threshold": 30, "cost_price": 18.0, "mrp": 99.0, "daily_velocity": 28, "status": "LOW"},
                {"sku": "NECKBAND-BT", "name": "Wireless Bluetooth Neckband", "category": "Audio", "stock": 5, "reorder_threshold": 12, "cost_price": 280.0, "mrp": 599.0, "daily_velocity": 6, "status": "LOW"},
                {"sku": "DATA-CABLE-BRAID", "name": "Braided 65W Type-C Cable", "category": "Cables", "stock": 35, "reorder_threshold": 15, "cost_price": 45.0, "mrp": 120.0, "daily_velocity": 12, "status": "HEALTHY"}
            ],
            "khata": [
                {"id": "KE1", "name": "Express Phone Repairs", "phone": "+91 98454 88990", "due_amount": 5400, "days_pending": 16, "last_reminder": "3 days ago", "notes": "Display combo & IC replacement", "risk": "Moderate"},
                {"id": "KE2", "name": "Anil Verma Gym", "phone": "+91 98450 99887", "due_amount": 1800, "days_pending": 8, "last_reminder": "2 days ago", "notes": "Earbuds & powerbank purchase", "risk": "Low"},
                {"id": "KE3", "name": "Smart Solutions Office", "phone": "+91 99115 66778", "due_amount": 2600, "days_pending": 5, "last_reminder": "Never", "notes": "HDMI cables & multi-plugs", "risk": "Low"}
            ],
            "hyperlocal_trends": [
                {"trend": "Type-C Fast Charging Surge", "change": "+55%", "type": "SURGE", "reason": "New phone purchases driving charger sales.", "action": "Stock up 40 units of 20W Fast Chargers on ONDC."},
                {"trend": "Tempered Glass Screen Protection", "change": "+42%", "type": "SURGE", "reason": "High footfall on SP road tech hub.", "action": "Reorder 100 assorted 9D screen protectors."},
                {"trend": "Micro-USB Legacy Cables", "change": "-65%", "type": "DEAD_STOCK", "reason": "Old standard phased out across modern phones.", "action": "Bundle free with phone repair service."}
            ],
            "ondc_distributors": [
                {"name": "SP Road Tech Wholesale ONDC", "distance_km": 0.8, "sku": "20W Type-C Fast Charger", "stock": "4 units (Critical)", "wholesale_price": 135.0, "mrp": 299.0, "action": "Reorder (30 units)", "qty": 30, "amt": "₹4,050"},
                {"name": "Nehru Place Electronics B2B", "distance_km": 3.4, "sku": "9D Tempered Glass Protector", "stock": "9 pcs (Low)", "wholesale_price": 16.5, "mrp": 99.0, "action": "Reorder (50 pcs)", "qty": 50, "amt": "₹825"},
                {"name": "Shenzhen India Direct ONDC", "distance_km": 4.2, "sku": "Wireless Bluetooth Neckband", "stock": "5 units (Low)", "wholesale_price": 265.0, "mrp": 599.0, "action": "Reorder (15 units)", "qty": 15, "amt": "₹3,975"}
            ]
        }
    }

    def __init__(self, default_biz: str = "kirana"):
        self.current_biz = default_biz if default_biz in self.BUSINESS_PROFILES else "kirana"
        self._load_business_profile(self.current_biz)

    def set_business_type(self, biz_type: str = "kirana") -> Dict[str, Any]:
        if biz_type in self.BUSINESS_PROFILES:
            self.current_biz = biz_type
        self._load_business_profile(self.current_biz)
        return {
            "business_type": self.current_biz,
            "merchant_profile": self.merchant_profile,
            "inventory_count": len(self.inventory),
            "khata_count": len(self.khata)
        }

    def _load_business_profile(self, biz_type: str):
        data = self.BUSINESS_PROFILES[biz_type]
        self.merchant_profile = data["merchant_profile"]
        self.inventory = data["inventory"]
        self.khata = data["khata"]
        self.hyperlocal_trends = data["hyperlocal_trends"]
        self.ondc_distributors = data["ondc_distributors"]

    # Multilingual Voice Responses across business categories
    def _get_response_text(self, intent: str, lang: str, **kwargs) -> str:
        lang = lang.lower().strip()
        biz = self.current_biz
        
        if intent == "SALES_SUMMARY":
            total = kwargs.get("total", f"{self.merchant_profile['today_collection']:,.0f}")
            count = kwargs.get("count", str(self.merchant_profile['today_txns']))
            top_item = kwargs.get("top_item", self.merchant_profile['top_item'])

            if lang == "telugu":
                return f"సేత్ గారూ, ఈరోజు మొత్తం ₹{total} కలెక్షన్ వచ్చింది ({count} లావాదేవీలు). అత్యధికంగా అమ్ముడైనది '{top_item}'. తక్కువ స్టాక్ ఉన్న వస్తువులను వెంటనే ONDC ద్వారా రీస్టాక్ చేయండి!"
            elif lang == "tamil":
                return f"சேத் அவர்களே, இன்று மொத்தம் ₹{total} வசூலாகியுள்ளது ({count} பரிவர்த்தனைகள்). அதிகம் விற்ற பொருள் '{top_item}'. குறைந்த இருப்பை உடனடியாக ONDC மூலம் ரீஸ்டாக் செய்யுங்கள்!"
            elif lang == "kannada":
                return f"ಸೇಠ್ ಅವರೇ, ಇಂದು ಒಟ್ಟು ₹{total} ಕಲೆಕ್ಷನ್ ಆಗಿದೆ ({count} ವಹಿವಾಟುಗಳು). ಅತಿ ಹೆಚ್ಚು ಮಾರಾಟವಾದದ್ದು '{top_item}'. ದಾಸ್ತಾನು ಕಡಿಮೆಯಿರುವ ವಸ್ತುಗಳನ್ನು ತಕ್ಷಣವೇ ONDC ಮೂಲಕ ಮರು-ಆರ್ಡರ್ ಮಾಡಿ!"
            elif lang == "hindi":
                return f"सेठ जी, आज कुल ₹{total} का कलेक्शन हुआ है ({count} transactions). सबसे ज़्यादा बिकने वाला आइटम '{top_item}' रहा। कम स्टॉक वाले सामान को ONDC से तुरंत रीस्टॉक करें!"
            else: # English
                return f"Boss, today's total collection reached ₹{total} across {count} transactions. The top-selling product was '{top_item}'. Restock recommendation generated via ONDC."

        elif intent == "INVENTORY_CHECK":
            items = kwargs.get("items", "3 items")
            if lang == "telugu":
                return f"మీ దుకాణంలో స్టాక్ తక్కువగా ఉంది: {items}. ONDC డిస్ట్రిబ్యూటర్ వద్ద హోల్‌సేల్ ధరలు సిద్ధంగా ఉన్నాయి. 1-క్లిక్‌తో ఆర్డర్ చేయండి."
            elif lang == "tamil":
                return f"கடையில் இருப்பு குறைவான பொருட்கள்: {items}. ONDC விநியோகஸ்தர் குறைந்த மொத்த விலையில் தருகிறார். உடனே ஆர்டர் செய்யலாம்."
            elif lang == "kannada":
                return f"ಅಂಗಡಿಯಲ್ಲಿ ದಾಸ್ತಾನು ಕಡಿಮೆಯಾಗಿದೆ: {items}. ONDC ಸಗಟು ವಿತರಕರು ಕಡಿಮೆ ದರದಲ್ಲಿ ನೀಡುತ್ತಿದ್ದಾರೆ. 1-ಕ್ಲಿಕ್ ಆರ್ಡರ್ ಸಿದ್ಧವಾಗಿದೆ."
            elif lang == "hindi":
                return f"दुकान में स्टॉक कम है: {items}. ONDC डिस्ट्रीब्यूटर से सबसे सस्ता थोक भाव मिल रहा है। तुरंत 1-क्लिक रीस्टॉक करें।"
            else:
                return f"Stock Alert: {items} are running below threshold. ONDC wholesale distributor has stock available for 1-click reorder."

        elif intent == "KHATA_RECOVERY":
            due = kwargs.get("due", "12,450")
            name = kwargs.get("name", "Anil Verma")
            cust_due = kwargs.get("cust_due", "4,850")
            days = kwargs.get("days", "18")
            if lang == "telugu":
                return f"మొత్తం ₹{due} పాత బకాయిలు ఉన్నాయి. అత్యధికంగా {name} వద్ద ₹{cust_due} ({days} రోజులుగా) పెండింగ్‌లో ఉంది. వాట్సాప్ ద్వారా పేటీఎం డైనమిక్ క్యూఆర్ లింక్ సిద్ధం చేశాను."
            elif lang == "tamil":
                return f"மொத்தம் ₹{due} கடன் பாக்கி உள்ளது. அதிகபட்சமாக {name} என்பவரிடம் ₹{cust_due} ({days} நாட்களாக) பாக்கி உள்ளது. வாட்ஸ்அப் பேடிஎம் UPI QR இணைப்பு தயார்."
            elif lang == "kannada":
                return f"ಒಟ್ಟು ₹{due} ಸಾಲದ ಹಣ ಬಾಕಿ ಇದೆ. ಗರಿಷ್ಠವಾಗಿ {name} ಅವರ ಬಳಿ ₹{cust_due} ({days} ದಿನಗಳಿಂದ) ಬಾಕಿ ಇದೆ. ವಾಟ್ಸಾಪ್ ಮೂಲಕ ಪೇಟಿಎಂ ಕ್ಯೂಆರ್ ಲಿಂಕ್ ಕಳುಹಿಸಲು ಸಿದ್ಧ."
            elif lang == "hindi":
                return f"कुल ₹{due} का पुराना उधार फंसा है। सबसे पुराना {name} का ₹{cust_due} ({days} दिन से) बाकी है। व्हाट्सएप पर डायनामिक पेटीएम क्यूआर लिंक तैयार है।"
            else:
                return f"Total trapped udhar is ₹{due}. Oldest pending is {name} with ₹{cust_due} ({days} days overdue). WhatsApp dynamic UPI payment link is ready to send."

        elif intent == "CREDIT_APPROVAL":
            limit = kwargs.get("limit", f"{self.merchant_profile['credit_limit']:,.0f}")
            if lang == "telugu":
                return f"అభినందనలు! మీ పేటీఎం సౌండ్‌బాక్స్ లావాదేవీల వేగం ఆధారంగా మీకు ₹{limit} తక్షణ వర్కింగ్ క్యాపిటల్ లోన్ 180 సెకన్లలో ముందస్తు ఆమోదం లభించింది."
            elif lang == "tamil":
                return f"வாழ்த்துகள்! உங்கள் பேடிஎம் சவுண்ட்பாக்ஸ் அடிப்படையில் ₹{limit} உடனடி மூலதனக் கடன் 180 வினாடிகளில் முன்அனுமதி வழங்கப்பட்டுள்ளது."
            elif lang == "kannada":
                return f"ಅಭಿನಂದನೆಗಳು! ನಿಮ್ಮ ಪೇಟಿಎಂ ಸೌಂಡ್‌ಬಾಕ್ಸ್ ಆಧಾರದ ಮೇಲೆ ₹{limit} ತ್ವರಿತ ಸಾಲ 180 ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಮುಂಚಿತವಾಗಿ ಮಂಜೂರಾಗಿದೆ."
            elif lang == "hindi":
                return f"बधाई हो! आपके पेटीएम साउंडबॉक्स ट्रांजैक्शन के आधार पर ₹{limit} का इंस्टेंट वर्किंग कैपिटल लोन 180 सेकंड में प्री-अप्रूव्ड मिला है।"
            else:
                return f"Congratulations! Based on your verified Paytm Soundbox velocity, you are pre-approved for ₹{limit} in instant 180-second working capital credit."

        else: # GENERAL_ASSIST
            store = self.merchant_profile["store_name"]
            if lang == "telugu":
                return f"నమస్కారం! {store} పేటీఎం సౌండ్‌బాక్స్ 4.0 సిద్ధంగా ఉంది. సేల్స్, స్టాక్, ఉధార్ లేదా లోన్ గురించి ఏదైనా అడగండి."
            elif lang == "tamil":
                return f"வணக்கம்! {store} பேடிஎம் சவுண்ட்பாக்ஸ் 4.0 தயாராக உள்ளது. விற்பனை, இருப்பு, கடன் பற்றி கேளுங்கள்."
            elif lang == "kannada":
                return f"ನಮಸ್ಕಾರ! {store} ಪೇಟಿಎಂ ಸೌಂಡ್‌ಬಾಕ್ಸ್ 4.0 ಸಿದ್ಧವಾಗಿದೆ. ಕಲೆಕ್ಷನ್, ದಾಸ್ತಾನು ಅಥವಾ ಸಾಲದ ಬಗ್ಗೆ ಕೇಳಿ."
            elif lang == "hindi":
                return f"नमस्ते! {store} पेटीएम साउंडबॉक्स 4.0 तैयार है। बिक्री, स्टॉक, उधारी या लोन के बारे में कुछ भी पूछें।"
            else:
                return f"Hello! {store} Paytm Soundbox 4.0 is active. Ask anything regarding sales, inventory, udhar, or loans."

    # Process Spoken Voice Query
    def process_query(self, query: str, language: str = "english", business_type: str = None) -> Dict[str, Any]:
        if business_type and business_type in self.BUSINESS_PROFILES and business_type != self.current_biz:
            self.set_business_type(business_type)

        q_lower = query.lower().strip()
        lang = language.lower().strip()

        # Sales intent
        if any(w in q_lower for w in ["munafa", "collection", "today", "aaj", "sales", "earnings", "total", "లబ్ది", "కలెక్షన్", "సేల్స్", "మొత్తం", "ఈరోజు", "मुनाफा", "बिक्री", "कलेक्शन", "आज", "வசூல்", "விற்பனை", "இன்று", "ಆದಾಯ", "ಕಲೆಕ್ಷನ್", "ಮಾರಾಟ", "ಇಂದು"]):
            total_today = self.merchant_profile["today_collection"]
            txn_count = self.merchant_profile["today_txns"]
            top_item = self.merchant_profile["top_item"]
            resp = self._get_response_text("SALES_SUMMARY", lang, total=f"{total_today:,.0f}", count=str(txn_count), top_item=top_item)
            return {
                "intent": "SALES_SUMMARY",
                "language": lang,
                "business_type": self.current_biz,
                "voice_response": resp,
                "metrics": {
                    "total_sales": total_today,
                    "txn_count": txn_count,
                    "top_item": top_item,
                    "avg_ticket": round(total_today / txn_count, 1)
                },
                "recommended_action": {
                    "type": "RESTOCK_ALERT",
                    "text": f"Restock fast-selling {top_item} via ONDC",
                    "sku": self.inventory[0]["sku"]
                }
            }

        # Loan intent check
        elif any(w in q_lower for w in ["loan", "credit", "paisa", "working capital", "paise", "borrow", "రుణం", "లోన్", "పరిమితి", "తక్షణ", "लोन", "ऋण", "क्रेडिट", "लिमिट", "கடன்", "லோன்", "வரம்பு", "முன்அனுமதி", "ಸಾಲ", "ಸಾಲದ ಮಿತಿ", "ಲೋನ್", "ಮಿತಿ", "ತ್ವರಿತ"]):
            return self.evaluate_merchant_credit(lang)

        # Inventory intent
        elif any(w in q_lower for w in ["stock", "khatam", "order", "inventory", "reorder", "milk", "butter", "dolo", "charger", "kurti", "ondc", "స్టాక్", "సరుకు", "ఆర్డర్", "పాలు", "స్టాక్‌లో", "మందులు", "स्टॉक", "सामान", "आर्डर", "दूध", "दवा", "थोक", "இருப்பு", "பொருட்கள்", "ஆர்டர்", "பால்", "மருந்து", "விலை", "ದಾಸ್ತಾನು", "ಸ್ಟಾಕ್", "ಹಾಲು", "ಔಷಧಿ", "ಆರ್ಡರ್", "ದರ"]):
            low_stock = [item for item in self.inventory if item["stock"] <= item["reorder_threshold"]]
            low_stock_names = ", ".join([f"{item['name']} ({item['stock']})" for item in low_stock])
            resp = self._get_response_text("INVENTORY_CHECK", lang, items=low_stock_names)
            return {
                "intent": "INVENTORY_CHECK",
                "language": lang,
                "business_type": self.current_biz,
                "voice_response": resp,
                "low_stock_items": low_stock,
                "recommended_action": {
                    "type": "ONDC_PURCHASE",
                    "text": f"1-Click Order {self.ondc_distributors[0]['sku']} ({self.ondc_distributors[0]['amt']})",
                    "sku": self.inventory[0]["sku"],
                    "estimated_amount": self.ondc_distributors[0]["amt"]
                }
            }

        # Udhar intent
        elif any(w in q_lower for w in ["udhar", "khata", "due", "pending", "reminder", "sharma", "anil", "verma", "mehra", "clinic", "boutique", "repair", "అప్పు", "బాకీ", "బకాయి", "రిమైండర్", "ఉధార్", "उधार", "बाकी", "खाता", "रिमाइंडर", "பாக்கி", "நினைவூட்டல்", "அனில்", "ಬಾಕಿ", "ಖಾತೆ", "ರಿಮೈಂಡರ್"]):
            total_due = sum(k["due_amount"] for k in self.khata)
            oldest = max(self.khata, key=lambda x: x["days_pending"])
            resp = self._get_response_text("KHATA_RECOVERY", lang, due=f"{total_due:,}", name=oldest["name"], cust_due=f"{oldest['due_amount']:,}", days=str(oldest["days_pending"]))
            return {
                "intent": "KHATA_RECOVERY",
                "language": lang,
                "business_type": self.current_biz,
                "voice_response": resp,
                "total_due": total_due,
                "top_defaulter": oldest,
                "recommended_action": {
                    "type": "SEND_WHATSAPP_REMINDER",
                    "text": f"Send 1-Click WhatsApp payment link to {oldest['name']}",
                    "target_customer": oldest["name"]
                }
            }

        # General intent
        else:
            resp = self._get_response_text("GENERAL_ASSIST", lang)
            return {
                "intent": "GENERAL_ASSIST",
                "language": lang,
                "business_type": self.current_biz,
                "voice_response": resp,
                "soundbox_status": self.merchant_profile["soundbox_status"],
                "store_name": self.merchant_profile["store_name"]
            }

    # Generate Udhar reminder in specified language with Dynamic UPI Deep Link
    def generate_udhar_reminder(self, customer_id: str, language: str = "english") -> Dict[str, Any]:
        customer = next((k for k in self.khata if k["id"] == customer_id or k["name"].lower() in customer_id.lower()), self.khata[0])
        upi_id = self.merchant_profile["upi_id"]
        amt = customer["due_amount"]
        store = self.merchant_profile["store_name"]
        
        upi_link = f"upi://pay?pa={upi_id}&pn={store.replace(' ', '%20')}&am={amt}&cu=INR&tn=Bill%20Settlement"
        web_pay_link = f"https://paytm.me/pay/{upi_id.split('@')[0]}?amt={amt}&cust={customer['id']}"

        lang = language.lower()
        if lang == "telugu":
            msg = f"నమస్కారం {customer['name']} గారూ, {store} నుండి మీ పాత ఖాతా బాకీ ₹{amt:,} చెల్లించవలసి ఉంది. దయచేసి క్రింది పేటీఎం లింక్ లేదా క్యూఆర్ కోడ్ ద్వారా వెంటనే సులభంగా చెల్లించండి: {web_pay_link} ధన్యవాదాలు!"
        elif lang == "tamil":
            msg = f"வணக்கம் {customer['name']} அவர்களே, {store} இல் உங்கள் நிலுவைத் தொகை ₹{amt:,} செலுத்த வேண்டியுள்ளது. இந்த பேடிஎம் UPI இணைப்பு மூலம் உடனடியாக செலுத்தவும்: {web_pay_link} நன்றி!"
        elif lang == "kannada":
            msg = f"ನಮಸ್ಕಾರ {customer['name']} ಅವರೇ, {store} ನಲ್ಲಿ ನಿಮ್ಮ ಹಳೆ ಬಾಕಿ ₹{amt:,} ಪಾವತಿಸಬೇಕಿದೆ. ದಯವಿಟ್ಟು ಈ ಪೇಟಿಎಂ ಲಿಂಕ್ ಮೂಲಕ ತಕ್ಷಣವೇ ಪಾವತಿಸಿ: {web_pay_link} ಧನ್ಯವಾದಗಳು!"
        elif lang == "hindi":
            msg = f"नमस्ते {customer['name']} जी, {store} की तरफ से आपकी पुरानी उधारी ₹{amt:,} बकाया है। कृपया इस पेटीएम लिंक के ज़रिए आसानी से भुगतान करें: {web_pay_link} धन्यवाद!"
        else:
            msg = f"Dear {customer['name']}, gentle reminder from {store} regarding your pending bill of ₹{amt:,} ({customer['days_pending']} days overdue). Please clear via Paytm instant UPI: {web_pay_link} Thank you!"

        return {
            "customer": customer,
            "whatsapp_message": msg,
            "upi_deep_link": upi_link,
            "web_pay_link": web_pay_link,
            "qr_payload": upi_link
        }

    # Execute Autonomous 1-Click ONDC Restock
    def execute_ondc_restock(self, sku: str, quantity: int, distributor_name: str = None) -> Dict[str, Any]:
        distributor = next((d for d in self.ondc_distributors if d["sku"] == sku), self.ondc_distributors[0])
        item = next((i for i in self.inventory if i["sku"] == sku), self.inventory[0])
        unit_price = distributor["wholesale_price"]
        total_cost = unit_price * quantity

        self.merchant_profile["account_balance"] -= total_cost
        item["stock"] += quantity
        item["status"] = "HEALTHY"

        return {
            "status": "SUCCESS",
            "order_id": f"ONDC-B2B-{sku[:4]}-889",
            "item_name": item["name"],
            "quantity_ordered": quantity,
            "distributor": distributor["name"],
            "unit_price": unit_price,
            "total_amount_deducted": total_cost,
            "new_merchant_balance": self.merchant_profile["account_balance"],
            "new_stock_level": item["stock"],
            "delivery_eta": "45 mins (Hyperlocal B2B Rider Assigned)"
        }

    # Real-Time Credit Underwriting via Soundbox Velocity
    def evaluate_merchant_credit(self, language: str = "english") -> Dict[str, Any]:
        limit = self.merchant_profile["credit_limit"]
        resp = self._get_response_text("CREDIT_APPROVAL", language, limit=f"{limit:,.0f}")
        return {
            "intent": "CREDIT_APPROVAL",
            "language": language,
            "business_type": self.current_biz,
            "pre_approved_limit": limit,
            "disbursal_window_seconds": 180,
            "interest_rate_monthly": 1.15,
            "repayment_model": "Daily Auto-Deduction from Soundbox Settlements (₹250/day)",
            "underwriting_factors": {
                "soundbox_active_days": 184,
                "daily_average_txns": self.merchant_profile["today_txns"],
                "zero_bounce_rate": "100%",
                "qr_collection_consistency": "98.4%"
            },
            "voice_response": resp
        }
