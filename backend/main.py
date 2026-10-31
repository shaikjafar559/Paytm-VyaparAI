import os
import base64
import time
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from .mock_db import (
    STORE_PROFILE,
    TODAY_METRICS,
    INVENTORY_ITEMS,
    HOURLY_SALES,
    RECENT_TRANSACTIONS,
    KHATA_LEDGER,
    LOAN_CREDIT_INSIGHTS,
    PAYTM_BUSINESS_UNIT_ECONOMICS
)
from .ai_engine import process_merchant_query
from .tts_service import synthesize_speech

app = FastAPI(title="Paytm Vyapar AI - 10/10 Merchant Growth Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class ChatRequest(BaseModel):
    query: str
    lang: Optional[str] = "auto"
    voice_gender: Optional[str] = "male"

class SoundboxSimulateRequest(BaseModel):
    amount: float = 500.0
    payer_name: Optional[str] = "Amit Sharma"

class KhataReminderRequest(BaseModel):
    customer_id: str
    phone: str
    amount: float

class LoanApplyRequest(BaseModel):
    amount: float = 250000.0
    tenure_months: int = 12

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/dashboard")
async def get_dashboard_data():
    return {
        "store": STORE_PROFILE,
        "metrics": TODAY_METRICS,
        "inventory": INVENTORY_ITEMS,
        "hourly_sales": HOURLY_SALES,
        "recent_transactions": RECENT_TRANSACTIONS,
        "khata_ledger": KHATA_LEDGER,
        "loan_insights": LOAN_CREDIT_INSIGHTS,
        "unit_economics": PAYTM_BUSINESS_UNIT_ECONOMICS
    }

@app.post("/api/chat")
async def chat_copilot(req: ChatRequest):
    result = process_merchant_query(req.query)
    
    # Synthesize speech
    audio_data_uri = None
    try:
        audio_bytes = await synthesize_speech(
            text=result["voice_text"],
            lang=result.get("lang", "auto"),
            voice_gender=req.voice_gender or "male"
        )
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_data_uri = f"data:audio/mp3;base64,{audio_b64}"
    except Exception as e:
        print(f"[TTS Error in API]: {e}")
        audio_data_uri = None

    return {
        "success": True,
        "query": req.query,
        "intent": result["intent"],
        "display_text": result["display_text"],
        "voice_text": result["voice_text"],
        "lang": result["lang"],
        "action": result.get("action", {}),
        "audio_data_uri": audio_data_uri
    }

@app.post("/api/soundbox/simulate")
async def simulate_soundbox(req: SoundboxSimulateRequest):
    amount_int = int(req.amount)
    
    soundbox_phrase = f"पेटीएम पर {amount_int} रुपये प्राप्त हुए!"
    ai_tip = f"बढ़िया! आज का कुल कलेक्शन अब ₹{TODAY_METRICS['total_revenue'] + amount_int:,} हो चुका है।"
    
    combined_speech = f"{soundbox_phrase} {ai_tip}"
    
    audio_bytes = await synthesize_speech(text=combined_speech, lang="hi", voice_gender="female")
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    
    TODAY_METRICS["total_revenue"] += amount_int
    TODAY_METRICS["upi_revenue"] += amount_int
    TODAY_METRICS["soundbox_verified_txns"] += 1
    
    RECENT_TRANSACTIONS.insert(0, {
        "time": "Just now",
        "amount": amount_int,
        "customer": req.payer_name or "Customer",
        "method": "Paytm Soundbox",
        "items": "Direct UPI Payment"
    })
    
    return {
        "success": True,
        "amount": amount_int,
        "soundbox_text": soundbox_phrase,
        "ai_tip": ai_tip,
        "audio_data_uri": f"data:audio/mp3;base64,{audio_b64}",
        "new_total": TODAY_METRICS["total_revenue"]
    }

@app.post("/api/khata/reminder")
async def send_khata_reminder(req: KhataReminderRequest):
    return {
        "success": True,
        "message": f"व्हाट्सएप पेमेंट लिंक (+91 {req.phone[-5:]}...) को भेज दिया गया है। ग्राहक लिंक पर क्लिक करके सीधे पेटीएम यूपीआई से भुगतान कर सकता है।",
        "payment_url": f"https://p.paytm.me/pay?vpa=sharmastore@paytm&am={req.amount}"
    }

@app.post("/api/vision/scan-bill")
async def scan_bill_invoice():
    """
    Simulates optical invoice parsing of wholesale distributor parcha
    and auto-stocks the items into the inventory.
    """
    scanned_items = [
        {"item": "Amul Taaza Milk 500ml", "qty_added": 30, "cost_unit": 24.5, "supplier": "M/s Gupta Wholesalers"},
        {"item": "Fortune Mustard Oil 1L", "qty_added": 24, "cost_unit": 132.0, "supplier": "M/s Gupta Wholesalers"},
        {"item": "Maggi 2-Minute Noodles", "qty_added": 50, "cost_unit": 11.5, "supplier": "M/s Gupta Wholesalers"}
    ]
    
    # Update inventory
    for sc in scanned_items:
        for inv in INVENTORY_ITEMS:
            if sc["item"].split()[0] in inv["name"]:
                inv["current_stock"] += sc["qty_added"]
                inv["status"] = "healthy"
                
    voice_msg = "थोक बिल स्कैन सफल! अमूल दूध के 30 पैकेट, फॉर्च्यून तेल की 24 बोतलें और मैगी के 50 पैकेट इन्वेंटरी में जोड़ दिए गए हैं।"
    audio_bytes = await synthesize_speech(text=voice_msg, lang="hi")
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "success": True,
        "invoice_number": "INV-GPT-2026-881",
        "supplier": "M/s Gupta FMCG Wholesalers, Sector 9 Noida",
        "total_invoice_amount": 4475,
        "items_extracted": scanned_items,
        "voice_text": voice_msg,
        "audio_data_uri": f"data:audio/mp3;base64,{audio_b64}",
        "updated_inventory": INVENTORY_ITEMS
    }

@app.post("/api/loan/disburse")
async def disburse_loan(req: LoanApplyRequest):
    """
    Simulates instant loan sanction and disbursement within 120 seconds.
    """
    txn_ref = f"PTM-LN-{int(time.time())}"
    voice_msg = f"बधाई हो! ₹{int(req.amount):,} का लोन आपके पेटीएम पेमेंट्स बैंक खाते में तुरंत ट्रांसफर कर दिया गया है। दैनिक भुगतान ₹320 साउंडबॉक्स से सेटल होगा।"
    audio_bytes = await synthesize_speech(text=voice_msg, lang="hi")
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "success": True,
        "loan_ref": txn_ref,
        "sanctioned_amount": req.amount,
        "disbursed_to": STORE_PROFILE["bank_account"],
        "daily_deduction": "₹320 / day via Soundbox",
        "voice_text": voice_msg,
        "audio_data_uri": f"data:audio/mp3;base64,{audio_b64}",
        "message": f"Loan amount of ₹{int(req.amount):,} credited to {STORE_PROFILE['bank_account']}"
    }

@app.post("/api/reorder")
async def trigger_reorder():
    return {
        "success": True,
        "message": "आर्डर सफलतापूर्वक थोक डिस्ट्रीब्यूटर (M/s Gupta Distributors, Noida) को व्हाट्सएप पर भेज दिया गया है। डिलीवरी कल सुबह 9 बजे होगी।",
        "po_number": "PO-PTM-2026-9042",
        "total_estimated_cost": 4850
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
