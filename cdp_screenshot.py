import asyncio
import subprocess
import time
import requests
import json
import base64
import os
import websockets

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
port = 9225
user_data = r"d:\KPMG\.edge_temp_profile"

async def main():
    print("Launching Edge headless...")
    proc = subprocess.Popen([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "--window-size=1280,900",
        "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait for CDP
        for _ in range(10):
            await asyncio.sleep(1)
            try:
                r = requests.get(f"http://localhost:{port}/json/version", timeout=1)
                if r.status_code == 200:
                    break
            except Exception:
                pass

        r_new = requests.put(f"http://localhost:{port}/json/new?about:blank")
        target = r_new.json()
        ws_url = target.get('webSocketDebuggerUrl')

        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cmd = {"id": msg_id, "method": method, "params": params or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('id') == cmd['id']:
                        return res.get('result', {})

            await send("Page.enable")
            await send("Runtime.enable")
            
            print("Navigating to https://dev187180.service-now.com/fnx ...")
            await send("Page.navigate", {"url": "https://dev187180.service-now.com/fnx"})

            print("Waiting 6 seconds for AngularJS rendering...")
            await asyncio.sleep(6)

            # Evaluate DOM text
            dom_check = await send("Runtime.evaluate", {
                "expression": "JSON.stringify({brand: document.querySelector('.fnx-brand-text')?.innerText, hero: document.querySelector('h1')?.innerText, bodyTextLen: document.body.innerText.length})"
            })
            print("DOM Evaluation:", dom_check.get('result', {}).get('value'))

            # Take screenshot
            shot = await send("Page.captureScreenshot", {"format": "png"})
            data = base64.b64decode(shot['data'])
            with open("d:/KPMG/portal_verified_screenshot.png", "wb") as f:
                f.write(data)
            print(f"Saved screenshot: d:/KPMG/portal_verified_screenshot.png ({len(data)} bytes)")

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(main())
