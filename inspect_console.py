import asyncio
import subprocess
import requests
import json
import websockets

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
port = 9226
user_data = r"d:\KPMG\.edge_temp_profile2"

async def main():
    proc = subprocess.Popen([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        await asyncio.sleep(2)
        r_new = requests.put(f"http://localhost:{port}/json/new?about:blank")
        ws_url = r_new.json().get('webSocketDebuggerUrl')

        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cmd = {"id": msg_id, "method": method, "params": params or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                return cmd['id']

            await send("Console.enable")
            await send("Runtime.enable")
            await send("Page.enable")
            await send("Page.navigate", {"url": "https://dev187180.service-now.com/fnx"})

            print("Listening for browser events...")
            start_t = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_t < 8:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    msg = json.loads(raw)
                    method = msg.get('method')
                    if method == 'Runtime.exceptionThrown':
                        print("[EXCEPTION]", msg['params']['exceptionDetails'])
                    elif method == 'Runtime.consoleAPICalled':
                        t = msg['params']['type']
                        args = [a.get('value') or a.get('description') for a in msg['params']['args']]
                        print(f"[CONSOLE {t}]", *args)
                except asyncio.TimeoutError:
                    pass

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(main())
