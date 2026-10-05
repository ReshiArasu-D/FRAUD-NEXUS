import asyncio, subprocess, requests, json, websockets, sys
sys.stdout.reconfigure(encoding='utf-8')

async def check():
    port = 9299
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--remote-debugging-port={port}',
        '--no-first-run', '--no-default-browser-check',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r = requests.put(f'http://localhost:{port}/json/new?about:blank')
        ws_url = r.json().get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send(m, p=None):
                nonlocal msg_id
                cmd = {'id': msg_id, 'method': m, 'params': p or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('id') == cmd['id']: return res

            await send('Page.enable')
            await send('Runtime.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)
            
            expr = "Array.from(document.querySelectorAll('button, a')).map(b => ({tag: b.tagName, text: b.innerText, cls: b.className}))"
            r = await send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            for item in r.get('result', {}).get('result', {}).get('value', []):
                print(item)
    finally:
        proc.kill()

asyncio.run(check())
