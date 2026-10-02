import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9246',
        '--no-first-run', '--no-default-browser-check',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile22',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9246/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')

        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cmd = {'id': msg_id, 'method': method, 'params': params or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                return cmd['id']

            await send('Console.enable')
            await send('Runtime.enable')
            await send('Page.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})

            print("Capturing console and errors during navigation...")
            start_t = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_t < 10:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    m = json.loads(raw)
                    method = m.get('method')
                    if method == 'Runtime.exceptionThrown':
                        print("[EXCEPTION]", json.dumps(m['params']['exceptionDetails'], indent=2))
                    elif method == 'Runtime.consoleAPICalled':
                        args = [str(a.get('value', a.get('description', ''))) for a in m['params']['args']]
                        print(f"[{m['params']['type']}]", " ".join(args))
                except asyncio.TimeoutError:
                    pass

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
