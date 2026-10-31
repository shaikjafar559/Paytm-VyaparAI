"""
Comprehensive Mock Database & Enterprise State for Paytm Vyapar AI.
Complete with Khata (Customer Udhaar), Visual Bill Invoices, Soundbox 3.0 Hardware telemetry,
and Paytm Merchant Lending Unit Economics.
"""

STORE_PROFILE = {
    "store_name": "Sharma Super Store",
    "owner_name": "Rajesh Sharma",
    "merchant_id": "PTM_MERCHANT_8839201",
    "city": "Noida, Sector 18",
    "category": "Grocery & FMCG Kirana",
    "paytm_soundbox_connected": True,
    "soundbox_device_id": "SBOX-IND-4091",
    "soundbox_model": "Paytm Soundbox 3.0 with LCD Display",
    "soundbox_battery": 88,
    "soundbox_sim_status": "4G Dual eSIM Active",
    "upi_vpa": "sharmastore@paytm",
    "bank_account": "Paytm Payments Bank **** 4812",
    "joined_since": "March 2021"
}

TODAY_METRICS = {
    "total_revenue": 28450,
    "upi_revenue": 24250,
    "soundbox_verified_txns": 128,
    "cash_revenue": 4200,
    "total_transactions": 149,
    "avg_ticket_size": 190.9,
    "comparison_vs_last_week": "+18.4%",
    "peak_sales_hour": "7:00 PM - 9:00 PM",
    "pending_khata_due": 3650
}

INVENTORY_ITEMS = [
    {
        "id": "INV-101",
        "name": "Amul Taaza Milk 500ml",
        "name_hi": "अमूल ताज़ा दूध (500ml)",
        "category": "Dairy",
        "current_stock": 4,
        "reorder_threshold": 15,
        "unit": "Packets",
        "price": 27,
        "cost": 24.5,
        "status": "critical_low",
        "daily_burn_rate": 22
    },
    {
        "id": "INV-102",
        "name": "Fortune Mustard Oil 1L",
        "name_hi": "फॉर्च्यून सरसों का तेल (1L)",
        "category": "Cooking Oils",
        "current_stock": 3,
        "reorder_threshold": 10,
        "unit": "Bottles",
        "price": 145,
        "cost": 132,
        "status": "critical_low",
        "daily_burn_rate": 7
    },
    {
        "id": "INV-103",
        "name": "Maggi 2-Minute Noodles 70g",
        "name_hi": "मैगी 2-मिनट नूडल्स (70g)",
        "category": "Packaged Food",
        "current_stock": 8,
        "reorder_threshold": 25,
        "unit": "Packets",
        "price": 14,
        "cost": 11.5,
        "status": "low",
        "daily_burn_rate": 28
    },
    {
        "id": "INV-104",
        "name": "Aashirvaad Shudh Chakki Atta 5kg",
        "name_hi": "आशीर्वाद शुद्ध चक्की आटा (5kg)",
        "category": "Staples",
        "current_stock": 18,
        "reorder_threshold": 8,
        "unit": "Bags",
        "price": 245,
        "cost": 220,
        "status": "healthy",
        "daily_burn_rate": 5
    },
    {
        "id": "INV-105",
        "name": "Tata Salt 1kg",
        "name_hi": "टाटा नमक (1kg)",
        "category": "Staples",
        "current_stock": 26,
        "reorder_threshold": 12,
        "unit": "Packets",
        "price": 28,
        "cost": 23,
        "status": "healthy",
        "daily_burn_rate": 6
    },
    {
        "id": "INV-106",
        "name": "Surf Excel Quick Wash 1kg",
        "name_hi": "सर्फ एक्सेल क्विक वॉश (1kg)",
        "category": "Household",
        "current_stock": 6,
        "reorder_threshold": 12,
        "unit": "Packs",
        "price": 160,
        "cost": 142,
        "status": "low",
        "daily_burn_rate": 4
    }
]

# DIGITAL KHATA / CUSTOMER UDHAAR LEDGER
KHATA_LEDGER = [
    {
        "customer_id": "CUST-01",
        "name": "Ramesh Verma",
        "phone": "+91 98112 45890",
        "amount_due": 420,
        "days_pending": 12,
        "last_items": "2L Mustard Oil & 1 Bread",
        "status": "overdue",
        "reminder_status": "Ready to send"
    },
    {
        "customer_id": "CUST-02",
        "name": "Amit Patel (Flat 302)",
        "phone": "+91 98731 22901",
        "amount_due": 950,
        "days_pending": 18,
        "last_items": "Atta 5kg, Spices, Dairy",
        "status": "critical_overdue",
        "reminder_status": "Overdue reminder needed"
    },
    {
        "customer_id": "CUST-03",
        "name": "Sunita Sharma",
        "phone": "+91 99100 87342",
        "amount_due": 280,
        "days_pending": 4,
        "last_items": "Tata Tea Gold & Sugar",
        "status": "recent",
        "reminder_status": "Within grace period"
    },
    {
        "customer_id": "CUST-04",
        "name": "Vikas Mathur",
        "phone": "+91 98991 34109",
        "amount_due": 2000,
        "days_pending": 24,
        "last_items": "Monthly Grocery Advance",
        "status": "critical_overdue",
        "reminder_status": "Call required"
    }
]

HOURLY_SALES = [
    {"hour": "8 AM", "sales": 1200, "txns": 8},
    {"hour": "10 AM", "sales": 3400, "txns": 19},
    {"hour": "12 PM", "sales": 4100, "txns": 23},
    {"hour": "2 PM", "sales": 1900, "txns": 11},
    {"hour": "4 PM", "sales": 2850, "txns": 16},
    {"hour": "6 PM", "sales": 6200, "txns": 32},
    {"hour": "8 PM", "sales": 8800, "txns": 40}
]

RECENT_TRANSACTIONS = [
    {"time": "Just now", "amount": 340, "customer": "Rohan Verma", "method": "Paytm UPI", "items": "Atta, Bread"},
    {"time": "4 mins ago", "amount": 85, "customer": "Pooja Gupta", "method": "Paytm Soundbox", "items": "Milk & Biscuit"},
    {"time": "11 mins ago", "amount": 620, "customer": "Vikram Singh", "method": "Paytm QR", "items": "Mustard Oil, Spices"},
    {"time": "22 mins ago", "amount": 140, "customer": "Sunil Kumar", "method": "Paytm UPI", "items": "Snacks & Cold drink"}
]

LOAN_CREDIT_INSIGHTS = {
    "eligible": True,
    "pre_approved_amount": 250000,
    "max_limit": 500000,
    "interest_rate": "1.15% per month",
    "daily_deduction_via_soundbox": "₹320 / day",
    "credit_score_indicator": "Strong (98% QR Settlement Consistency)",
    "tenure_months": 12,
    "processing_fee": "0% (Festival Waiver)",
    "lending_partner": "Paytm Payments Bank / Clix Capital",
    "disbursement_time": "Immediate (under 120 seconds)"
}

PAYTM_BUSINESS_UNIT_ECONOMICS = {
    "merchant_retention_lift": "+34%",
    "soundbox_subscription_churn_reduction": "-42%",
    "lending_attach_rate": "18.5%",
    "average_loan_size": "₹1,85,000",
    "estimated_annual_margin_per_merchant": "₹14,200"
}
