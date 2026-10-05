import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def test_fnx_app():
    profile_dir = r'd:\KPMG\.edge_temp_profile_fnx'
    port = 9275
    
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

            print("Navigating...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # Now evaluate on .fnx-app
            js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope ? scope.c : null;
                if (!c) return { error: "NO_C" };
                
                return {
                    currentView: c.currentView,
                    adminModule: c.adminModule,
                    hasInitAnalyticsWorkspace: typeof c.initAnalyticsWorkspace === 'function',
                    hasFetchAnalyticsData: typeof c.fetchAnalyticsData === 'function',
                    hasProcessAnalyticsAggregation: typeof c.processAnalyticsAggregation === 'function'
                };
            })()
            """
            r = await send('Runtime.evaluate', {'expression': js, 'returnByValue': True})
            print("Scope eval:", json.dumps(r['result']['result'].get('value'), indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test_fnx_app())
