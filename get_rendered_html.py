import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9231',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile7', 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9231/json/new?https://dev187180.service-now.com/fnx')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
            await asyncio.sleep(6)
            cmd = {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.body.innerHTML'}}
            await ws.send(json.dumps(cmd))
            res = json.loads(await ws.recv())
            html = res['result']['result'].get('value', '')
            with open('d:/KPMG/live_rendered_body.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Saved live_rendered_body.html ({len(html)} bytes)")

            # Check if angular is loaded
            cmd2 = {'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': 'typeof angular !== "undefined" ? angular.version.full : "NO_ANGULAR"'}}
            await ws.send(json.dumps(cmd2))
            res2 = json.loads(await ws.recv())
            print("Angular version:", res2['result']['result'].get('value'))

            # Check if there are any errors in window
            cmd3 = {'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.$sp ? "SP_EXISTS" : "NO_SP"'}}
            await ws.send(json.dumps(cmd3))
            res3 = json.loads(await ws.recv())
            print("SP Object:", res3['result']['result'].get('value'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
