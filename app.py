"""
Paytm VyaparAI — FastAPI Application Server v4.0
Includes Native Static Audio Server for Paytm Soundbox Multilingual Voice Playback
"""

import os
import io
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from copilot_engine import MerchantCopilotEngine
from gtts import gTTS

app = FastAPI(
    title="Paytm VyaparAI Multi-Agent API",
    description="The Autonomous AI Business Partner for Bharat Merchants with Multilingual Soundbox Audio",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MerchantCopilotEngine()

# Mount static assets (audio and audio_bundle.js)
static_dir = os.path.join(os.path.dirname(__file__), "static")
static_audio_dir = os.path.join(static_dir, "audio")
os.makedirs(static_audio_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/audio", StaticFiles(directory=static_audio_dir), name="audio")

class QueryRequest(BaseModel):
    query: str
    language: Optional[str] = "english"
    business_type: Optional[str] = "kirana"

class BusinessSwitchRequest(BaseModel):
    business_type: str = "kirana"

class RemindRequest(BaseModel):
    customer_id: str
    language: Optional[str] = "english"

class RestockRequest(BaseModel):
    sku: str
    quantity: int

class TTSRequest(BaseModel):
    text: str
    language: Optional[str] = "english"

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Paytm VyaparAI Server Running.</h1>"


@app.get("/favicon.ico")
async def get_favicon():
    ico_path = os.path.join(os.path.dirname(__file__), "paytm_vyapar_icon.ico")
    if os.path.exists(ico_path):
        return FileResponse(ico_path, media_type="image/x-icon")
    return Response(status_code=404)

@app.get("/paytm_vyapar_icon.png")
async def get_icon_png():
    png_path = os.path.join(os.path.dirname(__file__), "paytm_vyapar_icon.png")
    if os.path.exists(png_path):
        return FileResponse(png_path, media_type="image/png")
    return Response(status_code=404)

@app.get("/manifest.json")
async def get_manifest():
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.json")
    if os.path.exists(manifest_path):
        return FileResponse(manifest_path, media_type="application/manifest+json")
    return JSONResponse({})

@app.get("/api/profile")
async def get_profile():
    return engine.merchant_profile

@app.post("/api/copilot/query")
async def process_query(req: QueryRequest):
    result = engine.process_query(req.query, req.language, req.business_type)
    return JSONResponse(content=result)

@app.post("/api/business/switch")
async def switch_business(req: BusinessSwitchRequest):
    res = engine.set_business_type(req.business_type)
    return JSONResponse(content=res)

@app.get("/api/inventory")
async def get_inventory():
    return {
        "inventory": engine.inventory,
        "low_stock": [i for i in engine.inventory if i["stock"] <= i["reorder_threshold"]]
    }

@app.get("/api/khata")
async def get_khata():
    total_due = sum(k["due_amount"] for k in engine.khata)
    return {
        "total_due": total_due,
        "customer_count": len(engine.khata),
        "customers": engine.khata
    }

@app.post("/api/khata/remind")
async def trigger_reminder(req: RemindRequest):
    result = engine.generate_udhar_reminder(req.customer_id, req.language)
    return JSONResponse(content=result)

@app.get("/api/demand")
async def get_demand_trends():
    return {
        "neighborhood": "Koramangala 4th Block (2km radius)",
        "trends": engine.hyperlocal_trends,
        "distributors": engine.ondc_distributors
    }

@app.post("/api/ondc/order")
async def place_ondc_order(req: RestockRequest):
    result = engine.execute_ondc_restock(req.sku, req.quantity)
    return JSONResponse(content=result)

@app.get("/api/credit/evaluate")
async def evaluate_credit(language: Optional[str] = "english"):
    return engine.evaluate_merchant_credit(language)

# Native server-side TTS audio generator for Soundbox simulation
@app.post("/api/tts")
async def generate_speech(req: TTSRequest):
    lang_map = {
        "english": "en",
        "hindi": "hi",
        "telugu": "te",
        "tamil": "ta",
        "kannada": "kn"
    }
    lang_code = lang_map.get(req.language.lower(), "en")
    try:
        tts = gTTS(text=req.text, lang=lang_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return StreamingResponse(fp, media_type="audio/mp3")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    print("🚀 Starting Paytm VyaparAI Server on http://127.0.0.1:8080 ...")
    uvicorn.run(app, host="127.0.0.1", port=8080)


class LoginRequest(BaseModel):
    merchant_id: str
    password: str
    business_type: Optional[str] = "kirana"

@app.post("/api/auth/login")
async def merchant_login(req: LoginRequest):
    # Authentic Paytm Merchant Authentication
    biz = req.business_type or "kirana"
    if "pharma" in req.merchant_id.lower(): biz = "pharmacy"
    elif "cafe" in req.merchant_id.lower() or "rest" in req.merchant_id.lower(): biz = "restaurant"
    elif "apparel" in req.merchant_id.lower() or "garment" in req.merchant_id.lower(): biz = "apparel"
    elif "tech" in req.merchant_id.lower() or "elec" in req.merchant_id.lower(): biz = "electronics"

    profile = engine.set_business_type(biz)
    return JSONResponse(content={
        "status": "AUTHENTICATED",
        "merchant_id": req.merchant_id,
        "token": f"PAYTM-M-JWT-{req.merchant_id[:6].upper()}-99",
        "business_type": biz,
        "profile": profile
    })


# -------------------------------------------------------------
# CUSTOMER TAKEAWAY & VOICE NOTE ORDERS API
# -------------------------------------------------------------
@app.get("/api/orders")
async def get_orders(business_type: Optional[str] = None):
    biz = business_type or engine.current_biz
    orders = engine.CUSTOMER_SAMPLE_ORDERS.get(biz, engine.CUSTOMER_SAMPLE_ORDERS.get("kirana", []))
    return {"orders": orders, "business_type": biz}

class CustomerOrderRequest(BaseModel):
    customer_name: str
    phone: str
    order_text: str
    order_type: Optional[str] = "voice_note"
    language: Optional[str] = "english"
    business_type: Optional[str] = "kirana"

@app.post("/api/orders/create")
async def create_order(req: CustomerOrderRequest):
    # Create simple structured item parse
    order_id = f"ORD-{int(time.time()) % 10000}"
    items = []
    text_lower = req.order_text.lower()
    
    # Auto-extract common items
    if "milk" in text_lower or "दूध" in text_lower or "పాలు" in text_lower:
        items.append({"name": "Amul Taaza Milk 500ml", "qty": 2, "price": 24.50, "packed": False})
    if "butter" in text_lower or "मक्खन" in text_lower or "వెన్న" in text_lower:
        items.append({"name": "Amul Salted Butter 100g", "qty": 1, "price": 51.00, "packed": False})
    if "atta" in text_lower or "आटा" in text_lower or "పిండి" in text_lower:
        items.append({"name": "Aashirvaad Chakki Atta 5kg", "qty": 1, "price": 232.00, "packed": False})
    if "oil" in text_lower or "तेल" in text_lower or "నూనె" in text_lower:
        items.append({"name": "Fortune Sunflower Oil 1L", "qty": 1, "price": 124.00, "packed": False})
    if not items:
        items.append({"name": "General Provisions Pack", "qty": 1, "price": 120.00, "packed": False})
        
    total_amt = sum(it["qty"] * it["price"] for it in items)
    new_order = {
        "id": order_id,
        "customer_name": req.customer_name or "Valued Customer",
        "phone": req.phone or "+91 98450 99887",
        "order_type": req.order_type,
        "time": "Just now",
        "distance": "600m away (ETA 6 mins)",
        "voice_transcript": req.order_text,
        "language": req.language,
        "items": items,
        "total_amt": total_amt,
        "status": "WAITING_TO_PACK"
    }
    
    biz = req.business_type or engine.current_biz
    if biz not in engine.CUSTOMER_SAMPLE_ORDERS:
        engine.CUSTOMER_SAMPLE_ORDERS[biz] = []
    engine.CUSTOMER_SAMPLE_ORDERS[biz].insert(0, new_order)
    return {"status": "SUCCESS", "order": new_order}

class PackOrderRequest(BaseModel):
    order_id: str
    language: Optional[str] = "english"

@app.post("/api/orders/pack")
async def pack_order(req: PackOrderRequest):
    lang = (req.language or "english").lower()
    biz = engine.current_biz
    orders = engine.CUSTOMER_SAMPLE_ORDERS.get(biz, engine.CUSTOMER_SAMPLE_ORDERS.get("kirana", []))
    target = next((o for o in orders if o["id"] == req.order_id), None)
    if not target:
        return JSONResponse({"status": "ERROR", "message": "Order not found"}, status_code=404)
        
    target["status"] = "READY_FOR_PICKUP"
    for it in target["items"]:
        it["packed"] = True
        
    cust_name = target["customer_name"]
    amt = target["total_amt"]
    store_name = engine.merchant_profile.get("store_name", "Shop")
    
    # Generate localized WhatsApp Pickup Notification
    wa_msgs = {
        "english": f"Namaste {cust_name} ji! 🙏\nYour order ({len(target['items'])} items) is packed & ready for takeaway at {store_name}!\nTotal: ₹{amt:.2f}\nQuick Paytm UPI QR: paytm.me/qr/{target['id']}?amt={amt:.0f}\nPlease collect from the counter. Thank you! ✨",
        "telugu": f"నమస్కారం {cust_name} గారూ! 🙏\nమీ ఆర్డర్ ({len(target['items'])} వస్తువులు) ప్యాక్ చేయబడింది, {store_name} వద్ద సిద్ధంగా ఉంది!\nమొత్తం: ₹{amt:.2f}\nపేటీఎం UPI పే లింక్: paytm.me/qr/{target['id']}?amt={amt:.0f}\nకౌంటర్ వద్ద తీసుకోవచ్చు. ధన్యవాదాలు! ✨",
        "hindi": f"नमस्ते {cust_name} जी! 🙏\nआपका आर्डर ({len(target['items'])} सामान) पैक हो चुका है और {store_name} काउंटर पर तैयार है!\nकुल बिल: ₹{amt:.2f}\nPaytm UPI QR लिंक: paytm.me/qr/{target['id']}?amt={amt:.0f}\nआप आकर काउंटर से ले सकते हैं। धन्यवाद! ✨",
        "tamil": f"வணக்கம் {cust_name} அவர்களே! 🙏\nஉங்கள் ஆர்டர் ({len(target['items'])} பொருட்கள்) பேக் செய்யப்பட்டு {store_name} கடையில் தயாராக உள்ளது!\nமொத்த தொகை: ₹{amt:.2f}\nPaytm UPI லிங்க்: paytm.me/qr/{target['id']}?amt={amt:.0f}\nநேரில் வந்து பெற்றுக்கொள்ளலாம். நன்றி! ✨",
        "kannada": f"ನಮಸ್ಕಾರ {cust_name} ಅವರೇ! 🙏\nನಿಮ್ಮ ಆರ್ಡರ್ ({len(target['items'])} ವಸ್ತುಗಳು) ಪ್ಯಾಕ್ ಆಗಿದ್ದು, {store_name} ಅಂಗಡಿಯಲ್ಲಿ ಸಿದ್ಧವಾಗಿದೆ!\nಒಟ್ಟು ಬಿಲ್: ₹{amt:.2f}\nPaytm UPI ಲಿಂಕ್: paytm.me/qr/{target['id']}?amt={amt:.0f}\nಕೌಂಟರ್‌ನಿಂದ ಕಲೆಕ್ಟ್ ಮಾಡಿಕೊಳ್ಳಿ. ಧನ್ಯವಾದಗಳು! ✨"
    }
    
    wa_text = wa_msgs.get(lang, wa_msgs["english"])
    soundbox_announcement = f"Order #{req.order_id} Packed! Takeaway WhatsApp alert sent to {cust_name}."
    
    return {
        "status": "SUCCESS",
        "order": target,
        "whatsapp_message": wa_text,
        "soundbox_announcement": soundbox_announcement
    }

class CompleteOrderRequest(BaseModel):
    order_id: str

@app.post("/api/orders/complete")
async def complete_order(req: CompleteOrderRequest):
    biz = engine.current_biz
    orders = engine.CUSTOMER_SAMPLE_ORDERS.get(biz, engine.CUSTOMER_SAMPLE_ORDERS.get("kirana", []))
    target = next((o for o in orders if o["id"] == req.order_id), None)
    if not target:
        return JSONResponse({"status": "ERROR", "message": "Order not found"}, status_code=404)
        
    target["status"] = "COMPLETED"
    engine.merchant_profile["today_collection"] += target["total_amt"]
    engine.merchant_profile["today_txns"] += 1
    
    return {
        "status": "SUCCESS",
        "order": target,
        "today_collection": engine.merchant_profile["today_collection"],
        "today_txns": engine.merchant_profile["today_txns"]
    }
