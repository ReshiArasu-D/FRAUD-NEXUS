import asyncio
import subprocess
import requests
import json
import websockets

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
port = 9227
user_data = r"d:\KPMG\.edge_temp_profile3"

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
        r_new = requests.put(f"http://localhost:{port}/json/new?https://dev187180.service-now.com/fnx")
        target = r_new.json()
        ws_url = target.get('webSocketDebuggerUrl')

        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cmd = {"id": msg_id, "method": method, "params": params or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('id') == cmd['id']:
                        return res.get('result', {})

            await asyncio.sleep(5)
            eval_res = await send("Runtime.evaluate", {
                "expression": "JSON.stringify({url: window.location.href, title: document.title, htmlLength: document.documentElement.outerHTML.length, bodyHTML: document.body.innerHTML.substring(0, 500)})"
            })
            val = eval_res.get('result', {}).get('value')
            print("Current Page State:", val)

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == '__main__':
    asyncio.run(main())
