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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9252',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile28',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9252/json/new?about:blank')
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

            # View 1: Portal Select
            await send('Runtime.evaluate', {
                'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.goToPortalSelect(); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            shot1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_portal_select.png', 'wb') as f:
                f.write(base64.b64decode(shot1['result']['data']))
            print("Saved screenshot_portal_select.png")

            # View 2: Login
            await send('Runtime.evaluate', {
                'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.goToAuth("login"); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            shot2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_login.png', 'wb') as f:
                f.write(base64.b64decode(shot2['result']['data']))
            print("Saved screenshot_login.png")

            # View 3: Register
            await send('Runtime.evaluate', {
                'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.goToAuth("register"); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            shot3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_register.png', 'wb') as f:
                f.write(base64.b64decode(shot3['result']['data']))
            print("Saved screenshot_register.png")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
