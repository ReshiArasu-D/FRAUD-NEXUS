import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9240',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile16', 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9240/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cmd = {'id': msg_id, 'method': method, 'params': params or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                return cmd['id']

            await send('Network.enable')
            await send('Page.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})

            print("Listening to network requests...")
            requests_log = []
            start_t = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_t < 8:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    msg = json.loads(raw)
                    if msg.get('method') == 'Network.responseReceived':
                        resp = msg['params']['response']
                        u = resp['url']
                        status = resp['status']
                        if 'api/now/sp' in u or 'page' in u or 'widget' in u or status >= 400:
                            print(f"[{status}] {u}")
                except asyncio.TimeoutError:
                    pass
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
