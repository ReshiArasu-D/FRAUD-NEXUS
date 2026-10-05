import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def verify_auth_fix():
    print("=== VERIFYING CUSTOMER LOGIN & REGISTER FIX ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_auth_fix_verify'
    port = 9286
    
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

            print("1. Loading portal...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # Switch to Customer Auth: Login
            print("2. Switching to Customer Login view...")
            login_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.currentView = 'auth';
                scope.c.authMode = 'login';
                scope.$apply();
                return "AUTH_LOGIN_ACTIVE";
            })()
            """
            await send('Runtime.evaluate', {'expression': login_js, 'returnByValue': True})
            await asyncio.sleep(2)

            # Check geometry of tabs, box, form
            check_geo_js = """
            (() => {
                const getRect = (sel) => {
                    const el = document.querySelector(sel);
                    if (!el) return null;
                    const r = el.getBoundingClientRect();
                    return { width: r.width, height: r.height, top: r.top, left: r.left };
                };
                return {
                    page: getRect('.fnx-auth-page'),
                    left: getRect('.fnx-auth-left'),
                    right: getRect('.fnx-auth-right'),
                    box: getRect('.fnx-auth-box'),
                    tabs: getRect('.fnx-auth-tabs'),
                    form: getRect('.fnx-auth-form')
                };
            })()
            """
            r_geo = await send('Runtime.evaluate', {'expression': check_geo_js, 'returnByValue': True})
            print("Geometry after fix:", json.dumps(r_geo['result']['result'].get('value'), indent=2))

            # Screenshot 1: Customer Login Page
            print("3. Capturing Customer Login screenshot...")
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/customer_login_fixed.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("   Saved d:/KPMG/customer_login_fixed.png")

            # Switch to Customer Auth: Register
            print("4. Switching to Customer Register tab...")
            reg_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.authMode = 'register';
                scope.$apply();
                return "AUTH_REGISTER_ACTIVE";
            })()
            """
            await send('Runtime.evaluate', {'expression': reg_js, 'returnByValue': True})
            await asyncio.sleep(1)

            # Screenshot 2: Customer Register Page
            print("5. Capturing Customer Register screenshot...")
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/customer_register_fixed.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("   Saved d:/KPMG/customer_register_fixed.png")

            print("=== VERIFICATION COMPLETE ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(verify_auth_fix())
