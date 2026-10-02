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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9247',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile23',
        'https://dev187180.service-now.com/fnx'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(4)
        targets = requests.get('http://localhost:9247/json/list').json()
        target = next((t for t in targets if 'dev187180.service-now.com/fnx' in t.get('url', '')), None)
        print("Found target:", target.get('title'), target.get('url'))
        ws_url = target.get('webSocketDebuggerUrl')

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

            # Wait 4 more seconds for AngularJS
            await asyncio.sleep(4)

            # Check DOM
            res = await send('Runtime.evaluate', {
                'expression': 'document.body.innerText',
                'returnByValue': True
            })
            val = res['result']['result'].get('value', '')
            print("=== BODY INNER TEXT ===")
            print(val[:1500])
            print("=======================")

            # Take screenshot
            shot_res = await send('Page.captureScreenshot', {'format': 'png'})
            shot_b64 = shot_res['result']['data']
            data = base64.b64decode(shot_b64)
            with open('d:/KPMG/real_portal_screenshot.png', 'wb') as f:
                f.write(data)
            print(f"Captured real screenshot: {len(data)} bytes")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
