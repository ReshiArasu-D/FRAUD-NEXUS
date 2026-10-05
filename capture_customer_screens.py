import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def capture_customer_screens():
    profile_dir = r'd:\KPMG\.edge_temp_profile_cust_screens'
    port = 9289
    
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

            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # 1. Login using c.loadDemoSession()
            login_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.loadDemoSession();
                scope.$apply();
                return "LOGGED_IN";
            })()
            """
            await send('Runtime.evaluate', {'expression': login_js, 'returnByValue': True})
            await asyncio.sleep(2)

            # Screenshot Dashboard
            scr_dash = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/test_cust_dash.png', 'wb') as f:
                f.write(base64.b64decode(scr_dash['result']['data']))
            print("Saved test_cust_dash.png")

            # Click Track Cases via actual button
            print("Clicking Track Cases...")
            click_track = """
            (() => {
                const navItems = Array.from(document.querySelectorAll('.fnx-nav-item'));
                const trackBtn = navItems.find(x => x.innerText.includes('Track Cases'));
                if (trackBtn) {
                    trackBtn.click();
                    return "CLICKED_TRACK";
                }
                return "TRACK_BTN_NOT_FOUND";
            })()
            """
            r_tr = await send('Runtime.evaluate', {'expression': click_track, 'returnByValue': True})
            print("Click result:", r_tr['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Screenshot Track Cases
            scr_tr = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/test_cust_track.png', 'wb') as f:
                f.write(base64.b64decode(scr_tr['result']['data']))
            print("Saved test_cust_track.png")

            # Check where .fnx-track-cases is and its computed style
            chk_tr_pos = """
            (() => {
                const tr = document.querySelector('.fnx-track-cases');
                if (!tr) return "TR_NOT_IN_DOM";
                const rect = tr.getBoundingClientRect();
                return {
                    inDOM: true,
                    rect: { top: rect.top, left: rect.left, width: rect.width, height: rect.height },
                    display: window.getComputedStyle(tr).display,
                    parentTag: tr.parentElement.tagName,
                    parentClass: tr.parentElement.className,
                    parentRect: tr.parentElement.getBoundingClientRect(),
                    parentOverflow: window.getComputedStyle(tr.parentElement).overflow
                };
            })()
            """
            r_pos = await send('Runtime.evaluate', {'expression': chk_tr_pos, 'returnByValue': True})
            print("Track Cases position & parent:", json.dumps(r_pos['result']['result'].get('value'), indent=2))

            # Click Evidence via actual button
            print("Clicking Evidence...")
            click_ev = """
            (() => {
                const navItems = Array.from(document.querySelectorAll('.fnx-nav-item'));
                const evBtn = navItems.find(x => x.innerText.includes('Evidence'));
                if (evBtn) {
                    evBtn.click();
                    return "CLICKED_EV";
                }
                return "EV_BTN_NOT_FOUND";
            })()
            """
            await send('Runtime.evaluate', {'expression': click_ev, 'returnByValue': True})
            await asyncio.sleep(2)

            scr_ev = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/test_cust_ev.png', 'wb') as f:
                f.write(base64.b64decode(scr_ev['result']['data']))
            print("Saved test_cust_ev.png")

            # Click Help via actual button
            print("Clicking Help & Support...")
            click_help = """
            (() => {
                const navItems = Array.from(document.querySelectorAll('.fnx-nav-item'));
                const helpBtn = navItems.find(x => x.innerText.includes('Help'));
                if (helpBtn) {
                    helpBtn.click();
                    return "CLICKED_HELP";
                }
                return "HELP_BTN_NOT_FOUND";
            })()
            """
            await send('Runtime.evaluate', {'expression': click_help, 'returnByValue': True})
            await asyncio.sleep(2)

            scr_help = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/test_cust_help.png', 'wb') as f:
                f.write(base64.b64decode(scr_help['result']['data']))
            print("Saved test_cust_help.png")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(capture_customer_screens())
