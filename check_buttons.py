import asyncio, subprocess, requests, json, websockets, sys
sys.stdout.reconfigure(encoding='utf-8')

async def check():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9291',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile61',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9291/json/new?about:blank')
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
            await asyncio.sleep(5)
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click()'})
            await asyncio.sleep(1.5)
            btns = await send('Runtime.evaluate', {'expression': 'JSON.stringify(Array.from(document.querySelectorAll("button")).map(b => b.innerText))'})
            print('BUTTONS ON PORTAL SELECT:', btns['result'].get('result', {}).get('value'))
            
            # Click Enter Customer Portal
            click_res = await send('Runtime.evaluate', {'expression': 'var b = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Enter Customer Portal")); if (b) { b.click(); "CLICKED"; } else { "NOT FOUND"; }'})
            print('CLICK RESULT:', click_res['result'].get('result', {}).get('value'))
            await asyncio.sleep(2)
            
            auth_box = await send('Runtime.evaluate', {'expression': 'JSON.stringify({authBox: !!document.querySelector(".fnx-auth-box"), authPage: !!document.querySelector(".fnx-auth-page"), bodyLen: document.body.innerText.length, bodySnippet: document.body.innerText.substring(0, 200)})'})
            print('AUTH BOX VISIBLE:', auth_box['result'].get('result', {}).get('value'))
    finally:
        proc.terminate()

asyncio.run(check())
