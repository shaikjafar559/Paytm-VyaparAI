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

# Mount static audio files
static_audio_dir = os.path.join(os.path.dirname(__file__), "static", "audio")
os.makedirs(static_audio_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=static_audio_dir), name="audio")

class QueryRequest(BaseModel):
    query: str
    language: Optional[str] = "english"

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

@app.get("/api/profile")
async def get_profile():
    return engine.merchant_profile

@app.post("/api/copilot/query")
async def process_query(req: QueryRequest):
    result = engine.process_query(req.query, req.language)
    return JSONResponse(content=result)

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
    print("🚀 Starting Paytm VyaparAI Server on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
