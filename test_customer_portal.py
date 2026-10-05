import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def test_customer_portal():
    profile_dir = r'd:\KPMG\.edge_temp_profile_cust_test'
    port = 9287
    
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

            print("Navigating to portal...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # Click Get Started
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(x => x.innerText.includes("Get Started")).click()'
            })
            await asyncio.sleep(1)

            # Click Citizen Portal
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(x => x.innerText.includes("Citizen")).click()'
            })
            await asyncio.sleep(1)

            # Click Try Demo / Quick Demo Login
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(x => x.innerText.includes("Try Demo") || x.innerText.includes("JUDGE ACCESS")).click()'
            })
            await asyncio.sleep(2)

            # Check state
            eval_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                return {
                    currentView: c.currentView,
                    user: c.user,
                    customer: c.customer,
                    casesCount: c.cases ? c.cases.length : -1,
                    showAI: c.showAI,
                    hasFnxContent: document.querySelector('.fnx-content') !== null,
                    mainHtmlSnippet: document.querySelector('.fnx-content') ? document.querySelector('.fnx-content').innerHTML.substring(0, 500) : 'NO_FNX_CONTENT'
                };
            })()
            """
            r1 = await send('Runtime.evaluate', {'expression': eval_js, 'returnByValue': True})
            print("Dashboard state:", json.dumps(r1['result']['result'].get('value'), indent=2))

            # Now test navigating to trackCases
            print("\n--- Testing c.navigate('trackCases') ---")
            track_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.navigate('trackCases');
                scope.$apply();
                return {
                    currentView: scope.c.currentView,
                    trackCasesElem: document.querySelector('.fnx-track-cases') !== null,
                    html: document.querySelector('.fnx-content') ? document.querySelector('.fnx-content').innerHTML.substring(0, 400) : 'EMPTY'
                };
            })()
            """
            r2 = await send('Runtime.evaluate', {'expression': track_js, 'returnByValue': True})
            print("Track Cases state:", json.dumps(r2['result']['result'].get('value'), indent=2))

            # Now test navigating to evidenceVault
            print("\n--- Testing c.navigate('evidenceVault') ---")
            ev_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.navigate('evidenceVault');
                scope.$apply();
                return {
                    currentView: scope.c.currentView,
                    evidenceElem: document.querySelector('.fnx-evidence-vault') !== null,
                    html: document.querySelector('.fnx-content') ? document.querySelector('.fnx-content').innerHTML.substring(0, 400) : 'EMPTY'
                };
            })()
            """
            r3 = await send('Runtime.evaluate', {'expression': ev_js, 'returnByValue': True})
            print("Evidence Vault state:", json.dumps(r3['result']['result'].get('value'), indent=2))

            # Now test navigating to help
            print("\n--- Testing c.navigate('help') ---")
            help_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.navigate('help');
                scope.$apply();
                return {
                    currentView: scope.c.currentView,
                    helpElem: document.querySelector('.fnx-help-view') !== null,
                    html: document.querySelector('.fnx-content') ? document.querySelector('.fnx-content').innerHTML.substring(0, 400) : 'EMPTY'
                };
            })()
            """
            r4 = await send('Runtime.evaluate', {'expression': help_js, 'returnByValue': True})
            print("Help state:", json.dumps(r4['result']['result'].get('value'), indent=2))

            # Check AI Assistant button / trigger
            ai_js = """
            (() => {
                const triggers = Array.from(document.querySelectorAll('*')).filter(x => x.innerText && x.innerText.includes('Ask FRAUDNEXUS AI'));
                return triggers.map(t => ({
                    tag: t.tagName,
                    className: t.className,
                    visible: t.offsetParent !== null,
                    rect: t.getBoundingClientRect()
                }));
            })()
            """
            r_ai = await send('Runtime.evaluate', {'expression': ai_js, 'returnByValue': True})
            print("\nAI Trigger elements in DOM:", json.dumps(r_ai['result']['result'].get('value'), indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test_customer_portal())
