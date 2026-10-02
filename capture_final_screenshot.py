import asyncio
import subprocess
import requests
import json
import websockets
import base64

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9251',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile27',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9251/json/new?about:blank')
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

            # Wait 8 seconds for complete render
            await asyncio.sleep(8)

            shot_res = await send('Page.captureScreenshot', {'format': 'png'})
            b64_data = shot_res['result']['data']
            data = base64.b64decode(b64_data)
            with open('d:/KPMG/final_portal_screenshot.png', 'wb') as f:
                f.write(data)
            print(f"Captured screenshot: {len(data)} bytes")

            eval_res = await send('Runtime.evaluate', {
                'expression': 'JSON.stringify({textLen: document.body.innerText.length, sampleText: document.body.innerText.substring(0, 300), brand: document.querySelector(".fnx-brand-text")?.innerText})',
                'returnByValue': True
            })
            print('Eval result:\n', eval_res['result']['result'].get('value'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
