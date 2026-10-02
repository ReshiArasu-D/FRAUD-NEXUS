import asyncio
import subprocess
import requests
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9265',
        '--no-first-run', '--no-default-browser-check',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9265/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 2, 'method': 'Page.navigate', 'params': {'url': 'https://dev187180.service-now.com/fnx'}}))
            await ws.recv()
            await asyncio.sleep(7)
            cmd = {
                'id': 3,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': 'JSON.stringify(Array.from(document.querySelectorAll("button, a")).map(b => b.innerText.trim()).filter(Boolean))',
                    'returnByValue': True
                }
            }
            await ws.send(json.dumps(cmd))
            res = json.loads(await ws.recv())
            print('Buttons/links:\n', res['result']['result'].get('value'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
