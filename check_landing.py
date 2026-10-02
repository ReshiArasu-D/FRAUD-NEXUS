import asyncio, subprocess, requests, json, websockets, base64

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9271',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile46',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9271/json/new?about:blank')
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
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx?id=fnx_home'})
            
            for i in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-landing-hero")'})
                val = chk.get('result', {}).get('result', {}).get('value')
                if val:
                    print(f'Landing hero detected at {i+1}s!')
                    break
            
            await asyncio.sleep(2)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_landing_verified.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print('Saved screenshot_landing_verified.png')
    finally:
        proc.terminate()

asyncio.run(test())
