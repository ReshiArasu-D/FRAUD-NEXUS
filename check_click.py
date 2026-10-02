import asyncio, subprocess, requests, json, websockets, sys
sys.stdout.reconfigure(encoding='utf-8')

async def check():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9294',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile64',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9294/json/new?about:blank')
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

            # Test click on Get Started with full MouseEvent
            click_eval = """
            (function() {
                var btn = document.querySelector(".fnx-hero-btns button");
                if (!btn) return "BUTTON NOT FOUND";
                var evt = new MouseEvent('click', { bubbles: true, cancelable: true, view: window });
                btn.dispatchEvent(evt);
                return "DISPATCHED";
            })()
            """
            r_click = await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click(); "OK";'})
            print('CLICK RAW:', r_click)
            await asyncio.sleep(1.5)

            view_chk = await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-portal-select h2").innerText'})
            print('VIEW AFTER CLICK 1:', view_chk['result']['result'].get('value'))

            # Click Enter Customer Portal
            click2 = await send('Runtime.evaluate', {'expression': 'var b = Array.from(document.querySelectorAll(".fnx-portal-card button")).find(b => b.innerText.includes("Enter Customer Portal")); if (b) { b.click(); "CLICKED 2"; } else { "NOT FOUND"; }'})
            print('CLICK 2 RESULT:', click2['result']['result'].get('value'))
            await asyncio.sleep(2)

            auth_chk = await send('Runtime.evaluate', {'expression': 'JSON.stringify({authBox: !!document.querySelector(".fnx-auth-box"), loginTab: !!document.querySelector(".fnx-auth-tabs button"), emailInput: !!document.querySelector("input[ng-model=\'c.authForm.email\']"), bodyText: document.body.innerText.substring(0, 150)})'})
            print('AUTH CHECK:', auth_chk['result']['result'].get('value'))
    finally:
        proc.terminate()

asyncio.run(check())
