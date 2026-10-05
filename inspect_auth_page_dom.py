import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_auth_page():
    profile_dir = r'd:\KPMG\.edge_temp_profile_auth_inspect'
    port = 9284
    
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

            print("Navigating to https://dev187180.service-now.com/fnx...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # Switch to auth view
            switch_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.currentView = 'auth';
                scope.c.authMode = 'login';
                scope.$apply();
                return "AUTH_VIEW_ACTIVE";
            })()
            """
            r_sw = await send('Runtime.evaluate', {'expression': switch_js, 'returnByValue': True})
            print("Switch result:", r_sw['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Dump element bounds & styles
            inspect_js = """
            (() => {
                const getInfo = (sel) => {
                    const el = document.querySelector(sel);
                    if (!el) return { selector: sel, found: false };
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    return {
                        selector: sel,
                        found: true,
                        rect: {
                            top: rect.top,
                            left: rect.left,
                            width: rect.width,
                            height: rect.height,
                            bottom: rect.bottom,
                            right: rect.right
                        },
                        style: {
                            display: style.display,
                            position: style.position,
                            flex: style.flex,
                            flexDirection: style.flexDirection,
                            justifyContent: style.justifyContent,
                            alignItems: style.alignItems,
                            overflow: style.overflow,
                            overflowY: style.overflowY,
                            height: style.height,
                            minHeight: style.minHeight,
                            maxHeight: style.maxHeight,
                            width: style.width,
                            maxWidth: style.maxWidth,
                            padding: style.padding,
                            margin: style.margin
                        }
                    };
                };

                return [
                    getInfo('.fnx-app'),
                    getInfo('.fnx-auth-page'),
                    getInfo('.fnx-auth-left'),
                    getInfo('.fnx-auth-right'),
                    getInfo('.fnx-auth-box'),
                    getInfo('.fnx-auth-tabs'),
                    getInfo('.fnx-auth-form'),
                    getInfo('.fnx-auth-form-header'),
                    getInfo('.fnx-back-to-portal')
                ];
            })()
            """
            r_info = await send('Runtime.evaluate', {'expression': inspect_js, 'returnByValue': True})
            print("Auth Elements Info:", json.dumps(r_info['result']['result'].get('value'), indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(inspect_auth_page())
