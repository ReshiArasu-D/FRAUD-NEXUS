import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9288',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1600,1050',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile_domcheck',
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
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx?id=fnx_home'})
            await asyncio.sleep(6)

            # Query DOM
            dom_check = """
            (() => {
                const fnxApp = document.querySelector(".fnx-app");
                const heroBtn = document.querySelector(".fnx-hero-btns button, .fnx-hero button");
                let scopeFound = false;
                if (fnxApp && window.angular) {
                    const s = angular.element(fnxApp).scope();
                    if (s && s.c) scopeFound = true;
                }
                return {
                    url: window.location.href,
                    hasFnxApp: !!fnxApp,
                    hasAngular: !!window.angular,
                    scopeFound: scopeFound,
                    heroBtnText: heroBtn ? heroBtn.innerText : null
                };
            })()
            """
            res = await send('Runtime.evaluate', {'expression': dom_check, 'returnByValue': True})
            print('DOM Check Result:', res['result']['result'].get('value'))
    finally:
        proc.terminate()

asyncio.run(check())
