import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def debug_analytics():
    profile_dir = r'd:\KPMG\.edge_temp_profile_debug'
    port = 9273
    
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
            
            # Listen to console messages
            async def print_console():
                while True:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=0.5)
                        msg = json.loads(raw)
                        if msg.get('method') == 'Runtime.consoleAPICalled':
                            args = [x.get('value', x.get('description', '')) for x in msg.get('params', {}).get('args', [])]
                            print("[CONSOLE]", " ".join(map(str, args)))
                    except asyncio.TimeoutError:
                        break

            print("1. Navigating...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)

            # Quick login
            login_js = """
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c;
                c.currentView = 'adminWorkspace';
                c.adminModule = 'analytics';
                scope.$apply();
                return "SWITCHED_TO_ANALYTICS";
            })()
            """
            r_sw = await send('Runtime.evaluate', {'expression': login_js, 'returnByValue': True})
            print("Switch:", r_sw['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Check scope
            check_js = """
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c;
                return {
                    hasInit: typeof c.initAnalyticsWorkspace === 'function',
                    hasFetch: typeof c.fetchAnalyticsData === 'function',
                    loading: c.analyticsLoading,
                    rawCasesLen: c.rawCasesList ? c.rawCasesList.length : -1,
                    filteredLen: c.activeFilteredCases ? c.activeFilteredCases.length : -1,
                    kpis: c.analyticsKPIs
                };
            })()
            """
            r_chk = await send('Runtime.evaluate', {'expression': check_js, 'returnByValue': True})
            print("Check:", json.dumps(r_chk['result']['result'].get('value'), indent=2))

            # Manually trigger c.fetchAnalyticsData and observe
            trig_js = """
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c;
                try {
                    c.initAnalyticsWorkspace();
                    return "TRIGGERED_OK";
                } catch(e) {
                    return "ERROR: " + e.message + " stack: " + e.stack;
                }
            })()
            """
            r_trig = await send('Runtime.evaluate', {'expression': trig_js, 'returnByValue': True})
            print("Trig:", r_trig['result']['result'].get('value'))
            await asyncio.sleep(4)

            # Check console
            await print_console()

            # Check scope again
            r_chk2 = await send('Runtime.evaluate', {'expression': check_js, 'returnByValue': True})
            print("Check after fetch:", json.dumps(r_chk2['result']['result'].get('value'), indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(debug_analytics())
