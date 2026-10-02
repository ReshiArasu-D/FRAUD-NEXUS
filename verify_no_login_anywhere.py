import asyncio
import subprocess
import requests
import json
import websockets
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9259',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile35',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9259/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cmd = {'id': msg_id, 'method': method, 'params': params or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                while True:
                    m = json.loads(await ws.recv())
                    if m.get('id') == cmd['id']:
                        return m

            await send('Page.enable')
            await send('Runtime.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)

            # View 1: Landing Page
            shot1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_landing_clean.png', 'wb') as f:
                f.write(base64.b64decode(shot1['result']['data']))
            print("Saved screenshot_landing_clean.png")

            # View 2: Click Get Started -> Portal Select
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-hero-btns button").click()'
            })
            await asyncio.sleep(2)
            shot2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_portal_select_clean.png', 'wb') as f:
                f.write(base64.b64decode(shot2['result']['data']))
            print("Saved screenshot_portal_select_clean.png")

            # Verify no 'Log in' text anywhere in header
            check_text = await send('Runtime.evaluate', {
                'expression': 'JSON.stringify({allLoginButtons: Array.from(document.querySelectorAll("button, a")).filter(el => (el.innerText || "").trim().toLowerCase() === "log in" || (el.innerText || "").trim().toLowerCase() === "login").map(el => el.outerHTML)})',
                'returnByValue': True
            })
            print("Login buttons on portalSelect view:\n", check_text['result']['result'].get('value'))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
