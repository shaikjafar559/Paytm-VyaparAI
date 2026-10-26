"""
Paytm VyaparAI — Terminal / CLI Interface
Multi-Language: English, Telugu, Hindi, Tamil, Kannada
Run with: python cli.py
"""

import sys
import io
from copilot_engine import MerchantCopilotEngine

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    engine = MerchantCopilotEngine()
    current_lang = "english"

    print("=" * 68)
    print("        PAYTM VYAPAR-AI : THE AUTONOMOUS MERCHANT COPILOT")
    print("   Languages: English | Telugu (తెలుగు) | Hindi (हिंदी) | Tamil (தமிழ்) | Kannada (ಕನ್ನಡ)")
    print("=" * 68)
    print(f"Store: {engine.merchant_profile['store_name']}")
    print(f"Owner: {engine.merchant_profile['owner']} | Soundbox: {engine.merchant_profile['soundbox_id']} (ONLINE)")
    print(f"Account Balance: Rs. {engine.merchant_profile['account_balance']:,.2f}")
    print("-" * 68)
    print("Switch Language commands:")
    print("  'lang english' | 'lang telugu' | 'lang hindi' | 'lang tamil' | 'lang kannada'")
    print("Sample Queries:")
    print("  1. 'Aaj ka total collection aur munafa kitna hua?'")
    print("  2. 'ఈరోజు కలెక్షన్ ఎంత?' (Telugu)")
    print("  3. 'Sharma ji ka udhar balance kitna hai?'")
    print("  4. 'Check my instant loan limit'")
    print("=" * 68)

    while True:
        try:
            query = input(f"\n[{current_lang.upper()} Soundbox Input] > ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "q"]:
                print("Exiting Paytm VyaparAI. Shubh Din!")
                break

            if query.lower().startswith("lang "):
                new_lang = query.lower().split(" ", 1)[1].strip()
                if new_lang in ["english", "telugu", "hindi", "tamil", "kannada"]:
                    current_lang = new_lang
                    print(f"--> Switched language to: {current_lang.upper()}")
                    continue

            result = engine.process_query(query, current_lang)
            print(f"\n[Paytm VyaparAI ({current_lang.upper()}) Voice Response]")
            print(f">> \"{result.get('voice_response', '')}\"")

            if "recommended_action" in result:
                act = result["recommended_action"]
                print(f"\n[AI Autonomous Action Triggered]: {act.get('type')}")
                print(f"   Details: {act.get('text')}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting Paytm VyaparAI. Shubh Din!")
            break

if __name__ == "__main__":
    main()
