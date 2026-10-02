import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9237',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile13', 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9237/json/new?https://dev187180.service-now.com/fnx')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
            await asyncio.sleep(6)
            cmd = {
                'id': 1,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': 'document.body.innerText',
                    'returnByValue': True
                }
            }
            await ws.send(json.dumps(cmd))
            res = json.loads(await ws.recv())
            print('CDP Result:', json.dumps(res, indent=2))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
