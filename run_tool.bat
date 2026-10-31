@echo off
chcp 65001 > nul
title Paytm VyaparAI — Autonomous Merchant Copilot
echo =====================================================================
echo           PAYTM VYAPAR-AI : TRACK 1 (MERCHANT GROWTH AI)
echo           Starting Backend Server & Interactive Dashboard...
echo =====================================================================
cd /d "%~dp0"
if not exist "app.py" cd /d "C:\Users\ShaikAli\.gemini\antigravity\scratch\paytm-merchant-growth-ai"

start http://127.0.0.1:8080
python app.py
pause
