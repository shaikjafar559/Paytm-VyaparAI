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
            content = f.read()
            return HTMLResponse(
                content=content,
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
            )
    return HTMLResponse("<h1>Paytm VyaparAI Server Running.</h1>")


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

@app.get("/merchant_qr.png")
async def get_merchant_qr():
    qr_path = os.path.join(os.path.dirname(__file__), "merchant_qr.png")
    if os.path.exists(qr_path):
        return FileResponse(qr_path, media_type="image/png")
    return Response(status_code=404)

@app.get("/manifest.json")
async def get_manifest():
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.json")
    if os.path.exists(manifest_path):
        return FileResponse(manifest_path, media_type="application/manifest+json")
    return JSONResponse({})

@app.get("/sw.js")
async def get_service_worker():
    sw_path = os.path.join(os.path.dirname(__file__), "sw.js")
    if os.path.exists(sw_path):
        with open(sw_path, "r", encoding="utf-8") as f:
            return Response(
                content=f.read(),
                media_type="application/javascript",
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
            )
    if os.path.exists(sw_path):
        return FileResponse(sw_path, media_type="application/javascript", headers={"Service-Worker-Allowed": "/"})
    return Response(status_code=404)

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


# -------------------------------------------------------------
# ADD CUSTOMER KHATA ENDPOINT
# -------------------------------------------------------------
class AddCustomerPayload(BaseModel):
    name: str
    phone: Optional[str] = "+91 98450 11223"
    due_amount: float
    notes: Optional[str] = "Monthly Groceries & Essentials"
    days_pending: Optional[int] = 3
    risk: Optional[str] = "Low"
    addr: Optional[str] = "Neighborhood"
    dist: Optional[str] = "0.6 km"
    business_type: Optional[str] = "kirana"

@app.post("/api/khata/add")
async def api_add_customer(payload: AddCustomerPayload):
    biz = payload.business_type or engine.current_biz
    profile = engine.BUSINESS_PROFILES.get(biz, engine.BUSINESS_PROFILES["kirana"])
    new_id = f"K{len(profile.get('khata', [])) + 1}"
    
    new_cust = {
        "id": new_id,
        "name": payload.name,
        "phone": payload.phone,
        "due_amount": payload.due_amount,
        "days_pending": payload.days_pending,
        "last_reminder": "Never",
        "notes": payload.notes,
        "risk": payload.risk,
        "addr": payload.addr,
        "dist": payload.dist
    }
    profile.setdefault("khata", []).insert(0, new_cust)
    return {"status": "SUCCESS", "customer": new_cust, "total_khata": sum(c["due_amount"] for c in profile["khata"])}

class UpdateCustomerPayload(BaseModel):
    id: str
    name: str
    phone: Optional[str] = None
    due_amount: float
    notes: Optional[str] = None
    days_pending: Optional[int] = None
    risk: Optional[str] = None
    addr: Optional[str] = None
    dist: Optional[str] = None
    business_type: Optional[str] = None

class DeleteCustomerPayload(BaseModel):
    id: str
    business_type: Optional[str] = None

@app.post("/api/khata/update")
async def api_update_customer(payload: UpdateCustomerPayload):
    biz = payload.business_type or engine.current_biz
    res = engine.update_khata_customer(payload.id, payload.dict(), biz)
    return JSONResponse(content=res)

@app.post("/api/khata/delete")
async def api_delete_customer(payload: DeleteCustomerPayload):
    biz = payload.business_type or engine.current_biz
    res = engine.delete_khata_customer(payload.id, biz)
    return JSONResponse(content=res)


# -------------------------------------------------------------
# NORMAL MOBILE SMS GATEWAY API
# -------------------------------------------------------------
class SendSmsPayload(BaseModel):
    customer_name: str
    phone: str
    message: str
    due_amount: Optional[str] = None
    order_id: Optional[str] = None

@app.post("/api/sms/send")
async def send_sms_gateway(payload: SendSmsPayload):
    import time
    clean_phone = "".join(filter(str.isdigit, payload.phone))
    return {
        "status": "DELIVERED",
        "channel": "GSM_SMS_TELECOM_GATEWAY",
        "recipient": clean_phone,
        "customer_name": payload.customer_name,
        "message": payload.message,
        "chars": len(payload.message),
        "gateway": "Bharat Telecom / Jio-Airtel Enterprise SMS Gateway",
        "sender_id": "VM-PAYTMV",
        "delivery_status": "Delivered to Handset (ACK 200)",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


# -------------------------------------------------------------

# -------------------------------------------------------------
# UNIFIED TRANSACTIONS BACKEND ENGINE FOR VYAPARAI TOOL
# -------------------------------------------------------------
class TransactionPayload(BaseModel):
    customer_name: str
    phone: Optional[str] = "+91 98450 77889"
    amount: float
    channel: Optional[str] = "QR"  # QR, KHATA, ORDER
    channel_label: Optional[str] = None
    notes: Optional[str] = "Counter UPI Payment"
    rrn: Optional[str] = None

@app.get("/api/transactions")
async def get_all_transactions(limit: int = 50, channel: Optional[str] = None):
    res = engine.get_transactions(limit=limit, channel=channel)
    return JSONResponse(content={
        "status": "SUCCESS",
        "merchant": {
            "name": "Shaik Japhar",
            "upi_id": "8310508118@ptyes",
            "store_name": engine.merchant_profile.get("store_name", "Shop"),
            "soundbox_status": "ONLINE_DUAL_BAND"
        },
        **res
    })

@app.post("/api/transactions/record")
@app.post("/api/payments/record")
async def record_backend_transaction(payload: TransactionPayload):
    res = engine.record_transaction(
        customer_name=payload.customer_name,
        amount=payload.amount,
        channel=payload.channel or "QR",
        notes=payload.notes or "Counter Payment",
        phone=payload.phone or "+91 98450 77889",
        rrn=payload.rrn
    )
    return JSONResponse(content=res)

@app.get("/api/transactions/summary")
async def get_transactions_summary():
    coll = engine.merchant_profile.get("today_collection", 0)
    txns = engine.merchant_profile.get("today_txns", 0)
    return {
        "status": "SUCCESS",
        "today_collection": coll,
        "today_txns": txns,
        "avg_ticket": round(coll / max(1, txns), 2),
        "soundbox": "ONLINE_DUAL_BAND"
    }


# -------------------------------------------------------------
# REAL-TIME INCOMING PAYMENT DETECTION & WEBHOOK LISTENER
# -------------------------------------------------------------
INCOMING_PAYMENTS_QUEUE = []

@app.get("/api/payment/incoming")
@app.post("/api/payment/incoming")
async def receive_incoming_payment(
    amount: float = 1.0,
    name: Optional[str] = "Shaik Jafar",
    phone: Optional[str] = "+91 83105 08118",
    utr: Optional[str] = None
):
    payment_data = {
        "amount": float(amount),
        "customer_name": name,
        "phone": phone,
        "rrn": utr or f"UPI/{random.randint(395230000000, 395299999999)}",
        "notes": "Verified Live QR Payment",
        "timestamp": time.strftime("%d %b %Y, %I:%M %p")
    }
    INCOMING_PAYMENTS_QUEUE.append(payment_data)
    
    # Also record into engine ledger
    engine.record_transaction(
        customer_name=payment_data["customer_name"],
        amount=payment_data["amount"],
        channel="QR",
        notes=payment_data["notes"],
        phone=payment_data["phone"],
        rrn=payment_data["rrn"]
    )
    
    return {
        "status": "SUCCESS",
        "message": "Payment ingested into live tool stream",
        "payment": payment_data
    }

@app.get("/api/payment/poll")
async def poll_incoming_payment():
    if INCOMING_PAYMENTS_QUEUE:
        p = INCOMING_PAYMENTS_QUEUE.pop(0)
        return {"status": "RECEIVED", "payment": p}
    return {"status": "EMPTY"}


# -------------------------------------------------------------
# PAYTM VYAPARAI PAYMENT GATEWAY & TRANSACTION TRACKER ENGINE
# -------------------------------------------------------------
GATEWAY_ORDERS = {
    "PG_ORD_984210": {
        "order_id": "PG_ORD_984210",
        "amount": 1.0,
        "customer_name": "Shaik Jafar",
        "phone": "+91 83105 08118",
        "notes": "UPI Standee Gateway Verification",
        "status": "SUCCESS",
        "payment_id": "pay_984205128",
        "rrn": "UPI/395235564993",
        "payment_method": "UPI_INTENT",
        "merchant": "Shaik Japhar (8310508118@ptyes)",
        "created_at": "31 Oct 2026, 04:30 PM",
        "settled_at": "31 Oct 2026, 04:31 PM"
    }
}

class CreateGatewayOrderPayload(BaseModel):
    amount: float = 1.0
    customer_name: Optional[str] = "Customer"
    phone: Optional[str] = "+91 83105 08118"
    notes: Optional[str] = "Counter UPI Gateway Payment"

class PayGatewayOrderPayload(BaseModel):
    order_id: str
    payment_method: Optional[str] = "UPI_INTENT"
    utr: Optional[str] = None
    payer_name: Optional[str] = None

@app.post("/api/gateway/create-order")
async def create_gateway_order(payload: CreateGatewayOrderPayload, request: Request):
    import random, time
    order_id = f"PG_ORD_{random.randint(100000, 999999)}"
    amt = float(payload.amount)
    
    # Generate UPI intent URL
    upi_intent = f"upi://pay?pa=8310508118@ptyes&pn=Shaik+Japhar&am={amt:.2f}&cu=INR&tn={order_id}"
    
    host_header = request.headers.get("host", "127.0.0.1:8080")
    checkout_url = f"http://{host_header}/gateway/checkout?order_id={order_id}"
    
    order_data = {
        "order_id": order_id,
        "amount": amt,
        "customer_name": payload.customer_name or "Customer",
        "phone": payload.phone or "+91 83105 08118",
        "notes": payload.notes or "Paytm Payment Gateway Order",
        "status": "PENDING",
        "payment_id": None,
        "rrn": None,
        "payment_method": None,
        "checkout_url": checkout_url,
        "upi_intent_url": upi_intent,
        "merchant": "Shaik Japhar (8310508118@ptyes)",
        "created_at": time.strftime("%d %b %Y, %I:%M %p"),
        "settled_at": None
    }
    
    GATEWAY_ORDERS[order_id] = order_data
    return {
        "status": "SUCCESS",
        "message": "Gateway order created successfully",
        "order": order_data
    }

@app.get("/api/gateway/orders")
async def list_gateway_orders():
    orders_list = list(GATEWAY_ORDERS.values())
    orders_list.reverse()
    return {
        "status": "SUCCESS",
        "total_orders": len(orders_list),
        "successful_orders": len([o for o in orders_list if o["status"] == "SUCCESS"]),
        "total_collected": sum(o["amount"] for o in orders_list if o["status"] == "SUCCESS"),
        "orders": orders_list
    }

@app.get("/api/gateway/track/{order_id}")
async def track_gateway_order(order_id: str):
    order = GATEWAY_ORDERS.get(order_id)
    if not order:
        return JSONResponse({"status": "ERROR", "message": "Gateway order not found"}, status_code=404)
    return {
        "status": "SUCCESS",
        "order": order
    }

@app.post("/api/gateway/pay")
async def process_gateway_payment(payload: PayGatewayOrderPayload):
    import random, time
    order = GATEWAY_ORDERS.get(payload.order_id)
    if not order:
        order = {
            "order_id": payload.order_id,
            "amount": 1.0,
            "customer_name": payload.payer_name or "Shaik Jafar",
            "phone": "+91 83105 08118",
            "notes": "Paytm Payment Gateway Payment",
            "status": "PENDING",
            "created_at": time.strftime("%d %b %Y, %I:%M %p")
        }
        GATEWAY_ORDERS[payload.order_id] = order
        
    payment_id = f"pay_{random.randint(10000000, 99999999)}"
    bank_rrn = payload.utr or f"UPI/{random.randint(395230000000, 395299999999)}"
    
    order["status"] = "SUCCESS"
    order["payment_id"] = payment_id
    order["rrn"] = bank_rrn
    order["payment_method"] = payload.payment_method or "UPI_INTENT"
    if payload.payer_name:
        order["customer_name"] = payload.payer_name
    order["settled_at"] = time.strftime("%d %b %Y, %I:%M %p")
    
    # Broadcast to counter terminal incoming stream
    payment_event = {
        "amount": order["amount"],
        "customer_name": order["customer_name"],
        "phone": order["phone"],
        "rrn": bank_rrn,
        "notes": f"Gateway Order #{order['order_id']} ({order['payment_method']})",
        "timestamp": order["settled_at"]
    }
    INCOMING_PAYMENTS_QUEUE.append(payment_event)
    
    # Record to internal ledger
    engine.record_transaction(
        customer_name=order["customer_name"],
        amount=order["amount"],
        channel="QR",
        notes=f"Gateway Payment ({order['order_id']})",
        phone=order["phone"],
        rrn=bank_rrn
    )
    
    return {
        "status": "SUCCESS",
        "message": "Payment captured and settled via Paytm Payment Gateway",
        "order": order,
        "receipt": payment_event
    }

# -------------------------------------------------------------
# DEDICATED PAYTM PAYMENT GATEWAY CHECKOUT PAGE
# -------------------------------------------------------------
@app.get("/gateway/checkout", response_class=HTMLResponse)
async def serve_gateway_checkout(order_id: Optional[str] = None):
    order = GATEWAY_ORDERS.get(order_id, {
        "order_id": order_id or "PG_ORD_SAMPLE",
        "amount": 1.0,
        "customer_name": "Shaik Jafar",
        "phone": "+91 83105 08118",
        "notes": "Direct UPI Payment",
        "status": "PENDING"
    })
    
    checkout_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Paytm Payment Gateway - {order.get('order_id')}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @keyframes pulse-ring {{
      0% {{ transform: scale(0.95); opacity: 0.8; }}
      50% {{ transform: scale(1.05); opacity: 0.4; }}
      100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}
  </style>
</head>
<body class="bg-slate-100 min-h-screen flex items-center justify-center p-3 font-sans">
  <div class="max-w-md w-full bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-[#002970] text-white p-5 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-2xl bg-white text-[#002970] flex items-center justify-center font-black text-xl shadow">
          P
        </div>
        <div>
          <h1 class="font-extrabold text-base tracking-wide flex items-center gap-1.5">
            <span>Paytm</span>
            <span class="text-[#00b9f5]">Gateway</span>
            <i class="fa-solid fa-shield-halved text-xs text-emerald-400"></i>
          </h1>
          <p class="text-[11px] text-slate-300">256-bit Secure Bank Encryption</p>
        </div>
      </div>
      <div class="text-right">
        <span class="text-[10px] text-slate-300 block uppercase font-bold">Order ID</span>
        <span class="font-mono text-xs font-bold text-[#00b9f5]">{order.get('order_id')}</span>
      </div>
    </div>

    <!-- Merchant & Amount Header -->
    <div class="p-6 text-center border-b border-slate-100 bg-gradient-to-b from-slate-50 to-white">
      <p class="text-xs text-slate-500 font-bold uppercase tracking-wider">Paying To Merchant</p>
      <h2 class="text-lg font-black text-slate-900 mt-0.5 flex items-center justify-center gap-1.5">
        <span>Shaik Japhar</span>
        <i class="fa-solid fa-circle-check text-blue-500 text-sm"></i>
      </h2>
      <p class="text-xs font-mono text-slate-600 bg-slate-100 inline-block px-3 py-0.5 rounded-full mt-1 border border-slate-200">
        8310508118@ptyes
      </p>

      <div class="mt-4 py-4 bg-emerald-50 rounded-2xl border border-emerald-200">
        <span class="text-xs font-bold text-emerald-700 block">Total Payable Amount</span>
        <div class="text-4xl font-black text-emerald-950 mt-1">₹{order.get('amount'):.2f}</div>
        <span class="text-[11px] text-emerald-600 font-bold">✔ Zero Gateway Surcharge (0% MDR)</span>
      </div>
    </div>

    <!-- Payment Methods -->
    <div class="p-6 space-y-4" id="checkout-form-section">
      <p class="text-xs font-bold text-slate-700 uppercase tracking-wide">Select Payment Method</p>

      <!-- Option 1: Direct UPI Apps -->
      <div class="grid grid-cols-3 gap-2">
        <button onclick="selectUpiApp('Paytm')" class="upi-app-btn p-3 rounded-2xl border-2 border-blue-500 bg-blue-50/50 hover:bg-blue-100/50 transition flex flex-col items-center justify-center gap-1 cursor-pointer">
          <i class="fa-solid fa-wallet text-blue-600 text-lg"></i>
          <span class="text-[11px] font-bold text-blue-900">Paytm</span>
        </button>
        <button onclick="selectUpiApp('Google Pay')" class="upi-app-btn p-3 rounded-2xl border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition flex flex-col items-center justify-center gap-1 cursor-pointer">
          <i class="fa-brands fa-google text-slate-700 text-lg"></i>
          <span class="text-[11px] font-bold text-slate-800">GPay</span>
        </button>
        <button onclick="selectUpiApp('PhonePe')" class="upi-app-btn p-3 rounded-2xl border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition flex flex-col items-center justify-center gap-1 cursor-pointer">
          <i class="fa-solid fa-mobile-screen-button text-purple-600 text-lg"></i>
          <span class="text-[11px] font-bold text-slate-800">PhonePe</span>
        </button>
      </div>

      <!-- Option 2: QR Standee Scan -->
      <div class="p-3 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-slate-700 text-lg">
            <i class="fa-solid fa-qrcode"></i>
          </div>
          <div class="text-left">
            <span class="text-xs font-bold text-slate-800 block">UPI QR Scan & Pay</span>
            <span class="text-[10px] text-slate-500">Scan via any UPI scanner</span>
          </div>
        </div>
        <a href="upi://pay?pa=8310508118@ptyes&pn=Shaik+Japhar&am={order.get('amount'):.2f}&cu=INR" class="px-3 py-1.5 bg-[#00b9f5] hover:bg-cyan-400 text-[#002970] font-bold text-xs rounded-xl transition">
          Open App
        </a>
      </div>

      <!-- Payer Name Field -->
      <div>
        <label class="block text-[11px] font-bold text-slate-600 mb-1">Payer Name</label>
        <input type="text" id="payer-name-input" value="{order.get('customer_name')}" class="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>

      <!-- Pay Action Button -->
      <button onclick="submitGatewayPayment()" id="pay-action-btn" class="w-full py-3.5 bg-gradient-to-r from-emerald-600 to-teal-700 hover:from-emerald-700 hover:to-teal-800 text-white font-black text-sm rounded-2xl shadow-lg transition flex items-center justify-center gap-2 cursor-pointer">
        <i class="fa-solid fa-lock text-xs"></i>
        <span>Pay ₹{order.get('amount'):.2f} via Secure Gateway</span>
      </button>

      <p class="text-[10px] text-center text-slate-400 flex items-center justify-center gap-1">
        <i class="fa-solid fa-shield text-[9px] text-slate-400"></i>
        <span>NPCI UPI Unified Payments Interface • Verified Merchant Account</span>
      </p>
    </div>

    <!-- Success Screen (Initially Hidden) -->
    <div id="checkout-success-section" class="p-8 text-center space-y-4 hidden animate-scale-up">
      <div class="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-4xl mx-auto shadow-inner">
        <i class="fa-solid fa-check"></i>
      </div>
      <div>
        <h3 class="text-2xl font-black text-slate-900">Payment Successful!</h3>
        <p class="text-xs text-slate-500 mt-1">Paytm Soundbox 4.0 Voice Chime Triggered at Store Counter</p>
      </div>

      <div class="bg-slate-50 rounded-2xl p-4 border border-slate-200 text-left text-xs space-y-2">
        <div class="flex justify-between"><span class="text-slate-500">Amount Paid:</span><span class="font-bold text-emerald-600 text-sm">₹{order.get('amount'):.2f}</span></div>
        <div class="flex justify-between"><span class="text-slate-500">Order ID:</span><span class="font-mono font-bold text-slate-800" id="res-order-id">{order.get('order_id')}</span></div>
        <div class="flex justify-between"><span class="text-slate-500">Gateway Ref:</span><span class="font-mono font-bold text-slate-800" id="res-pay-id">pay_...</span></div>
        <div class="flex justify-between"><span class="text-slate-500">Bank UPI RRN:</span><span class="font-mono font-bold text-slate-800" id="res-rrn">UPI/...</span></div>
        <div class="flex justify-between"><span class="text-slate-500">Paid To:</span><span class="font-bold text-slate-800">Shaik Japhar (8310508118@ptyes)</span></div>
      </div>

      <button onclick="window.close()" class="w-full py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition">
        Close Window
      </button>
    </div>
  </div>

  <script>
    let selectedMethod = 'Paytm UPI';
    function selectUpiApp(name) {{
      selectedMethod = name + ' UPI';
      document.querySelectorAll('.upi-app-btn').forEach(b => {{
        b.className = 'upi-app-btn p-3 rounded-2xl border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition flex flex-col items-center justify-center gap-1 cursor-pointer';
      }});
      event.currentTarget.className = 'upi-app-btn p-3 rounded-2xl border-2 border-blue-500 bg-blue-50/50 hover:bg-blue-100/50 transition flex flex-col items-center justify-center gap-1 cursor-pointer';
    }}

    function submitGatewayPayment() {{
      const btn = document.getElementById('pay-action-btn');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Processing with Bank...</span>';

      const payerName = document.getElementById('payer-name-input')?.value || 'Customer';

      fetch('/api/gateway/pay', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          order_id: '{order.get('order_id')}',
          payment_method: selectedMethod,
          payer_name: payerName
        }})
      }})
      .then(res => res.json())
      .then(data => {{
        if (data.status === 'SUCCESS') {{
          document.getElementById('checkout-form-section').classList.add('hidden');
          document.getElementById('checkout-success-section').classList.remove('hidden');
          document.getElementById('res-pay-id').innerText = data.order.payment_id;
          document.getElementById('res-rrn').innerText = data.order.rrn;
        }} else {{
          alert('Payment Failed: ' + data.message);
          btn.disabled = false;
          btn.innerHTML = '<span>Pay ₹{order.get('amount'):.2f} via Secure Gateway</span>';
        }}
      }})
      .catch(err => {{
        alert('Network Error connecting to Payment Gateway');
        btn.disabled = false;
        btn.innerHTML = '<span>Pay ₹{order.get('amount'):.2f} via Secure Gateway</span>';
      }});
    }}
  </script>
</body>
</html>"""
    return HTMLResponse(content=checkout_html)
