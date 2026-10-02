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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9262',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile38',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9262/json/new?about:blank')
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

            # Get coordinates of Get Started button
            box_res = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const btn = document.querySelector(".fnx-hero-btns button");
                    const rect = btn.getBoundingClientRect();
                    return JSON.stringify({ x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 });
                })()
                """,
                'returnByValue': True
            })
            coords = json.loads(box_res['result']['result'].get('value'))
            print("Get Started coords:", coords)

            # Click with CDP Input
            await send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
            await send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
            await asyncio.sleep(1.5)

            # Get coords of Enter Customer Portal button
            box_card = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Enter Customer Portal"));
                    if (!btn) return null;
                    const rect = btn.getBoundingClientRect();
                    return JSON.stringify({ x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 });
                })()
                """,
                'returnByValue': True
            })
            val_card = box_card['result']['result'].get('value')
            print("Customer Portal button coords:", val_card)
            if val_card:
                c2 = json.loads(val_card)
                await send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': c2['x'], 'y': c2['y'], 'button': 'left', 'clickCount': 1})
                await send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': c2['x'], 'y': c2['y'], 'button': 'left', 'clickCount': 1})
                await asyncio.sleep(1.5)

            # Take screenshot of Login with eye icon
            shot_login = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_real_login_eye.png', 'wb') as f:
                f.write(base64.b64decode(shot_login['result']['data']))
            print("Saved screenshot_real_login_eye.png")

            # Click Register tab
            box_reg = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const btn = Array.from(document.querySelectorAll(".fnx-auth-tabs button")).find(b => b.innerText.includes("Register"));
                    if (!btn) return null;
                    const rect = btn.getBoundingClientRect();
                    return JSON.stringify({ x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 });
                })()
                """,
                'returnByValue': True
            })
            val_reg = box_reg['result']['result'].get('value')
            print("Register tab coords:", val_reg)
            if val_reg:
                c3 = json.loads(val_reg)
                await send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': c3['x'], 'y': c3['y'], 'button': 'left', 'clickCount': 1})
                await send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': c3['x'], 'y': c3['y'], 'button': 'left', 'clickCount': 1})
                await asyncio.sleep(1)

            # Take screenshot of Register with eye icons
            shot_reg = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_real_register_eye.png', 'wb') as f:
                f.write(base64.b64decode(shot_reg['result']['data']))
            print("Saved screenshot_real_register_eye.png")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
