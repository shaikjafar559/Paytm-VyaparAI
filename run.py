import os
import sys
import uvicorn

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    sys.path.insert(0, current_dir)
    print("=" * 65)
    print("Starting Paytm VyaparAI - Autonomous Merchant Business Copilot")
    print("Local Web App: http://127.0.0.1:8080")
    print("=" * 65)
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
