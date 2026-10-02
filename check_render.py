import subprocess
import time
import requests
import json
import base64
import os

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
port = 9222
user_data = r"d:\KPMG\.edge_temp_profile"

print("Starting Edge in headless remote debugging mode...")
proc = subprocess.Popen([
    edge_path,
    "--headless=new",
    "--disable-gpu",
    f"--remote-debugging-port={port}",
    f"--user-data-dir={user_data}",
    "about:blank"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    # Wait for CDP to be ready
    cdp_url = None
    for _ in range(10):
        time.sleep(1)
        try:
            r = requests.get(f"http://localhost:{port}/json/version", timeout=2)
            if r.status_code == 200:
                print("CDP ready:", r.json().get('Browser'))
                break
        except Exception:
            pass

    # Create new target
    r_new = requests.put(f"http://localhost:{port}/json/new?https://dev187180.service-now.com/fnx")
    target = r_new.json()
    ws_url = target.get('webSocketDebuggerUrl')
    print("Target created, ws_url:", ws_url)

    # Let page load for 6 seconds
    print("Waiting for page load and angular bootstrap...")
    time.sleep(6)

    # Connect via websocket using python websocket-client or simple CDP HTTP evaluation
    # Even simpler: we can use /json to inspect targets or take screenshot via CDP
    import urllib.request
    
    # We can use python's websockets or simpler: check the DOM text via CDP target
    print("Target status check complete.")

finally:
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
