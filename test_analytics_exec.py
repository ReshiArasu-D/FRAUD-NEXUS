import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def test_analytics_exec():
    profile_dir = r'd:\KPMG\.edge_temp_profile_exec'
    port = 9276
    
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

            # Switch to analytics
            js_switch = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                c.currentView = 'adminWorkspace';
                c.setAdminModule('analytics');
                scope.$apply();
                return "SWITCHED";
            })()
            """
            r_sw = await send('Runtime.evaluate', {'expression': js_switch, 'returnByValue': True})
            print("Switch result:", r_sw['result']['result'].get('value'))

            # Wait 5 seconds for async API calls to complete
            await asyncio.sleep(5)

            # Check analytics state
            js_check = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                return {
                    loading: c.analyticsLoading,
                    totalCasesRaw: c.totalCasesRaw,
                    filteredCount: c.filteredCasesCount,
                    kpis: c.analyticsKPIs,
                    incidentTypesCount: c.incidentTypeStats ? c.incidentTypeStats.length : 0,
                    statusStatsCount: c.statusStats ? c.statusStats.length : 0,
                    trendPoints: c.trendData ? c.trendData.length : 0,
                    investigatorsCount: c.investigatorsList ? c.investigatorsList.length : 0,
                    clustersCount: c.fraudClusters ? c.fraudClusters.length : 0
                };
            })()
            """
            r_chk = await send('Runtime.evaluate', {'expression': js_check, 'returnByValue': True})
            print("Analytics State after API fetch:", json.dumps(r_chk['result']['result'].get('value'), indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test_analytics_exec())
