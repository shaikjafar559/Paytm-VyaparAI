import os
import io
import asyncio
import edge_tts
from gtts import gTTS

AUDIO_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "audio_cache")
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

VOICE_MAP = {
    "hi": "hi-IN-MadhurNeural",       # Natural Hindi male voice
    "hi-female": "hi-IN-SwaraNeural",  # Natural Hindi female voice
    "en": "en-IN-PrabhatNeural",      # Natural Indian English male
    "en-female": "en-IN-NeerjaNeural" # Natural Indian English female
}

def detect_language(text: str) -> str:
    """Detect if text contains Devanagari script or Hinglish markers."""
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return "hi"
    return "en"

async def synthesize_speech(text: str, lang: str = "auto", voice_gender: str = "male") -> bytes:
    """
    Synthesize speech using Microsoft Edge Neural TTS (with gTTS fallback).
    Returns audio/mpeg byte stream.
    """
    target_lang = detect_language(text) if lang == "auto" else lang
    voice_key = f"{target_lang}-female" if voice_gender == "female" else target_lang
    voice_name = VOICE_MAP.get(voice_key, VOICE_MAP["hi"])

    try:
        communicate = edge_tts.Communicate(text, voice_name)
        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        audio_stream.seek(0)
        return audio_stream.read()
    except Exception as e:
        print(f"[TTS Fallback to gTTS] EdgeTTS failed: {e}")
        # Fallback to gTTS
        buf = io.BytesIO()
        tts = gTTS(text=text, lang="hi" if target_lang == "hi" else "en")
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
