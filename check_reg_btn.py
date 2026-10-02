import asyncio, subprocess, requests, json, websockets, sys, time
sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9299',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile68',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9299/json/new?about:blank')
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
            
            # Wait for landing
            for _ in range(20):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-hero-btns button")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            # 1. Click Get Started
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click()'})
            await asyncio.sleep(1.5)

            # 2. Click Enter Customer Portal
            await send('Runtime.evaluate', {'expression': 'var b = Array.from(document.querySelectorAll(".fnx-portal-card button")).find(b => b.innerText.includes("Enter Customer Portal")); if (b) b.click();'})
            await asyncio.sleep(1.5)

            # 3. Click Register Tab
            await send('Runtime.evaluate', {'expression': 'var b = Array.from(document.querySelectorAll(".fnx-auth-tabs button")).find(b => b.innerText.includes("Register")); if (b) b.click();'})
            await asyncio.sleep(1.5)

            # Inspect all buttons in auth box
            btns = await send('Runtime.evaluate', {'expression': """
            JSON.stringify(Array.from(document.querySelectorAll(".fnx-auth-box button")).map(b => ({
                text: b.innerText.trim(),
                type: b.type,
                cls: b.className,
                disabled: b.disabled
            })))
            """})
            print("AUTH BOX BUTTONS:\n", btns['result']['result'].get('value'))

            # Also inspect all inputs in auth box
            inps = await send('Runtime.evaluate', {'expression': """
            JSON.stringify(Array.from(document.querySelectorAll(".fnx-auth-box input, .fnx-auth-box select, .fnx-auth-box textarea")).map(i => ({
                tag: i.tagName,
                model: i.getAttribute("ng-model"),
                type: i.type,
                required: i.required,
                pattern: i.pattern
            })))
            """})
            print("AUTH BOX INPUTS:\n", inps['result']['result'].get('value'))
    finally:
        proc.terminate()

asyncio.run(test())
