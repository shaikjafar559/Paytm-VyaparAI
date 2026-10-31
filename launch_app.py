# -*- coding: utf-8 -*-
"""
launch_app.py - Standalone Desktop Launcher for Paytm VyaparAI
Runs on dedicated port 8080 to prevent collision with other localhost projects.
Launches a dedicated standalone window in Microsoft Edge or Google Chrome.
"""
import os
import sys
import time
import socket
import subprocess
import webbrowser
import urllib.request

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8080
SERVER_URL = f"http://127.0.0.1:{PORT}/"
HEALTH_URL = f"http://127.0.0.1:{PORT}/api/profile"

def is_server_running(host="127.0.0.1", port=PORT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.8)
        res = sock.connect_ex((host, port))
        sock.close()
        return res == 0
    except Exception:
        return False

def start_backend_server():
    print(f"Starting Paytm VyaparAI backend server on port {PORT}...")
    cmd = [
        sys.executable,
        "-m", "uvicorn",
        "app:app",
        "--host", "127.0.0.1",
        "--port", str(PORT),
        "--app-dir", APP_DIR
    ]
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
    
    # Wait for server to become responsive
    for _ in range(25):
        time.sleep(0.4)
        try:
            req = urllib.request.urlopen(HEALTH_URL, timeout=1.0)
            if req.status == 200:
                print("Paytm VyaparAI backend is live!")
                return proc
        except Exception:
            pass
    return proc

def get_browser_app_cmd():
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
                "--window-size=1440,920"
            ]
    return None

def main():
    os.chdir(APP_DIR)
    
    # Ensure backend server on port 8080
    if not is_server_running():
        start_backend_server()
    else:
        print(f"Backend server is already running on port {PORT}.")

    # Open app window
    browser_cmd = get_browser_app_cmd()
    if browser_cmd:
        print(f"Launching desktop application: {browser_cmd[0]}")
        subprocess.Popen(browser_cmd)
    else:
        print("Opening default browser...")
        webbrowser.open(SERVER_URL)

if __name__ == "__main__":
    main()
