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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9265',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile40',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9265/json/new?about:blank')
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
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)
            shot_landing = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_landing_clean.png', 'wb') as f:
                f.write(base64.b64decode(shot_landing['result']['data']))
            print("Saved screenshot_landing_clean.png")

            # 1. Click 'Get Started'
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-hero-btns button").click()'
            })
            await asyncio.sleep(1.5)

            # 2. Click 'Enter Customer Portal'
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Enter Customer Portal")).click()'
            })
            await asyncio.sleep(1.5)

            # 3. Currently on Login tab -> Take screenshot
            shot_login = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_login_eye.png', 'wb') as f:
                f.write(base64.b64decode(shot_login['result']['data']))
            print("Saved screenshot_login_eye.png")

            # 4. Click 'Register' tab
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll(".fnx-auth-tabs button")).find(b => b.innerText.includes("Register")).click()'
            })
            await asyncio.sleep(1.5)

            # Type sample passwords
            await send('Runtime.evaluate', {
                'expression': """
                const p1 = document.querySelector('input[placeholder="Create password"]');
                const p2 = document.querySelector('input[placeholder="Confirm password"]');
                if (p1) { p1.value = 'DemoPass123!'; p1.dispatchEvent(new Event('input', {bubbles: true})); }
                if (p2) { p2.value = 'DemoPass123!'; p2.dispatchEvent(new Event('input', {bubbles: true})); }
                """
            })
            await asyncio.sleep(0.5)

            # Take screenshot of Register with eye icons
            shot_reg = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_register_eye.png', 'wb') as f:
                f.write(base64.b64decode(shot_reg['result']['data']))
            print("Saved screenshot_register_eye.png")

            # 5. Click the eye button on confirm password to toggle visibility
            await send('Runtime.evaluate', {
                'expression': 'document.querySelectorAll(".fnx-eye-btn")[1]?.click()'
            })
            await asyncio.sleep(0.5)

            shot_toggle = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_register_eye_toggled.png', 'wb') as f:
                f.write(base64.b64decode(shot_toggle['result']['data']))
            print("Saved screenshot_register_eye_toggled.png")

            check = await send('Runtime.evaluate', {
                'expression': 'JSON.stringify({eyeBtns: document.querySelectorAll(".fnx-eye-btn").length, types: Array.from(document.querySelectorAll(".fnx-password-wrap input")).map(i => i.type)})',
                'returnByValue': True
            })
            print("Check result:\n", check['result']['result'].get('value'))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
