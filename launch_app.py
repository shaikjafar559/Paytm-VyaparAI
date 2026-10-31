# -*- coding: utf-8 -*-
"""
launch_app.py - Standalone Desktop Launcher for Paytm VyaparAI
Starts FastAPI backend if not already running, and launches a dedicated native
desktop application window using Microsoft Edge or Google Chrome app mode.
"""
import os
import sys
import time
import socket
import subprocess
import webbrowser
import urllib.request

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_URL = "http://127.0.0.1:8000/"
HEALTH_URL = "http://127.0.0.1:8000/api/profile"

def is_server_running(host="127.0.0.1", port=8000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        res = sock.connect_ex((host, port))
        sock.close()
        return res == 0
    except Exception:
        return False

def start_backend_server():
    print("Starting Paytm VyaparAI backend server on port 8000...")
    cmd = [
        sys.executable,
        "-m", "uvicorn",
        "app:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--app-dir", APP_DIR
    ]
    # In Windows, use CREATE_NO_WINDOW if available to prevent black command prompt
    creation_flags = 0
    if os.name == 'nt' and hasattr(subprocess, 'CREATE_NO_WINDOW'):
        creation_flags = subprocess.CREATE_NO_WINDOW

    proc = subprocess.Popen(
        cmd,
        cwd=APP_DIR,
        creationflags=creation_flags,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait up to 10 seconds for server to be responsive
    for _ in range(20):
        time.sleep(0.5)
        try:
            req = urllib.request.urlopen(HEALTH_URL, timeout=1.0)
            if req.status == 200:
                print("Backend server is live and healthy!")
                return proc
        except Exception:
            pass
    print("Warning: Server took longer than expected to report healthy, continuing...")
    return proc

def get_browser_app_cmd():
    # Candidates for Chromium-based browser supporting --app flag
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    
    for path in candidates:
        if os.path.exists(path):
            return [
                path,
                f"--app={SERVER_URL}",
                "--window-size=1440,920",
                "--app-id=paytm-vyapar-ai"
            ]
    return None

def main():
    os.chdir(APP_DIR)
    
    # 1. Ensure backend is running
    if not is_server_running():
        start_backend_server()
    else:
        print("Backend server is already running on port 8000.")

    # 2. Launch App Window
    browser_cmd = get_browser_app_cmd()
    if browser_cmd:
        print(f"Launching desktop application window via: {browser_cmd[0]}")
        subprocess.Popen(browser_cmd)
    else:
        print("Opening default browser...")
        webbrowser.open(SERVER_URL)

if __name__ == "__main__":
    main()
