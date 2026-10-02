import asyncio, subprocess, requests, json, websockets

async def check():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9287',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile57',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9287/json/new?about:blank')
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
            await asyncio.sleep(6)
            
            # Click Get Started
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click()'})
            await asyncio.sleep(1.5)
            
            # Click Enter Customer Portal
            await send('Runtime.evaluate', {'expression': 'Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Enter Customer Portal")).click()'})
            await asyncio.sleep(2)

            dom = await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-auth-page") ? "AUTH PAGE FOUND" : ("BODY: " + (document.body ? document.body.innerHTML.substring(0, 300) : "NO BODY"))'})
            print('CHECK:', dom)

            cur_view = await send('Runtime.evaluate', {'expression': 'window.location.href'})
            print('CURRENT URL:', cur_view)
    finally:
        proc.terminate()

asyncio.run(check())
