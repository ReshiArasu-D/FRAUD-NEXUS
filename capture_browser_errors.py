import asyncio, subprocess, requests, json, websockets

async def check():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9288',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile58',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9288/json/new?about:blank')
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
            await send('Runtime.enable')
            await send('Log.enable')

            # Listen for messages
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx?id=fnx_home'})
            
            errors = []
            for _ in range(15):
                await asyncio.sleep(0.5)
                while True:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=0.2)
                        ev = json.loads(raw)
                        if ev.get('method') == 'Runtime.exceptionThrown':
                            errors.append(ev.get('params', {}).get('exceptionDetails', {}))
                        elif ev.get('method') == 'Runtime.consoleAPICalled':
                            t = ev.get('params', {}).get('type')
                            if t in ['error', 'warning']:
                                errors.append(ev.get('params', {}).get('args'))
                    except asyncio.TimeoutError:
                        break
            
            print("FOUND ERRORS:", len(errors))
            for err in errors[:10]:
                print("ERR:", err)
    finally:
        proc.terminate()

asyncio.run(check())
