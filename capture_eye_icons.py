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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9260',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile36',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9260/json/new?about:blank')
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

            # View Register tab
            await send('Runtime.evaluate', {
                'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.goToAuth("register"); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)

            # Type into password to demonstrate eye icon
            type_js = """
            const p1 = document.querySelector('input[placeholder="Create password"]');
            const p2 = document.querySelector('input[placeholder="Confirm password"]');
            if (p1) { p1.value = 'SecretPass123!'; p1.dispatchEvent(new Event('input', {bubbles: true})); }
            if (p2) { p2.value = 'SecretPass123!'; p2.dispatchEvent(new Event('input', {bubbles: true})); }
            """
            await send('Runtime.evaluate', {'expression': type_js})
            await asyncio.sleep(1)

            shot1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_register_with_eyes.png', 'wb') as f:
                f.write(base64.b64decode(shot1['result']['data']))
            print("Saved screenshot_register_with_eyes.png")

            # Click eye icon to reveal password
            click_eye_js = """
            const eyes = document.querySelectorAll('.fnx-eye-btn');
            if (eyes[0]) eyes[0].click();
            """
            await send('Runtime.evaluate', {'expression': click_eye_js})
            await asyncio.sleep(1)

            shot2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_register_revealed.png', 'wb') as f:
                f.write(base64.b64decode(shot2['result']['data']))
            print("Saved screenshot_register_revealed.png")

            # Check eye button count
            check_eyes = await send('Runtime.evaluate', {
                'expression': 'JSON.stringify({eyeBtnsCount: document.querySelectorAll(".fnx-eye-btn").length, inputTypes: Array.from(document.querySelectorAll(".fnx-password-wrap input")).map(i => i.type)})',
                'returnByValue': True
            })
            print("Eyes check:\n", check_eyes['result']['result'].get('value'))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
