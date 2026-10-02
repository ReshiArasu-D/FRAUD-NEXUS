import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9238',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile14', 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9238/json/new?about:blank')
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
                        return m.get('result', {})

            await send('Page.enable')
            await send('Runtime.enable')
            print("Navigating to https://dev187180.service-now.com/fnx ...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            # Wait for loadEventFired
            for _ in range(15):
                raw = await ws.recv()
                msg = json.loads(raw)
                if msg.get('method') == 'Page.loadEventFired':
                    print("Page.loadEventFired received!")
                    break
            
            # Wait an additional 4 seconds for AngularJS
            await asyncio.sleep(4)

            # Evaluate
            res = await send('Runtime.evaluate', {
                'expression': 'JSON.stringify({url: location.href, title: document.title, bodyText: document.body ? document.body.innerText.substring(0, 300) : "NO_BODY"})',
                'returnByValue': True
            })
            print('Evaluation:\n', res.get('result', {}).get('value'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
