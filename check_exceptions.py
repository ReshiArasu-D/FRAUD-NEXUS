import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_exceptions():
    profile_dir = r'd:\KPMG\.edge_temp_profile_ex'
    port = 9274
    
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--remote-debugging-port={port}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1680,1050',
        f'--user-data-dir={profile_dir}',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        await asyncio.sleep(2)
        r_new = requests.put(f'http://localhost:{port}/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        
        async with websockets.connect(ws_url, max_size=30000000) as ws:
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

            # Collect all errors
            errors = []
            async def listen_for_events(duration=6):
                end_time = asyncio.get_event_loop().time() + duration
                while asyncio.get_event_loop().time() < end_time:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=0.3)
                        msg = json.loads(raw)
                        if msg.get('method') == 'Runtime.exceptionThrown':
                            print("[EXCEPTION]", msg['params']['exceptionDetails'].get('text'), msg['params']['exceptionDetails'].get('exception', {}).get('description'))
                        elif msg.get('method') == 'Runtime.consoleAPICalled':
                            t = msg['params'].get('type')
                            if t in ['error', 'warning']:
                                args = [x.get('value', x.get('description', '')) for x in msg['params'].get('args', [])]
                                print(f"[CONSOLE {t.upper()}]", " ".join(map(str, args)))
                    except asyncio.TimeoutError:
                        pass

            print("Navigating...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await listen_for_events(8)
            print("Done checking initial load.")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(check_exceptions())
