import asyncio, subprocess, requests, json, websockets, base64, sys, os

sys.stdout.reconfigure(encoding='utf-8')

async def test_customer():
    print("=== TESTING CUSTOMER PORTAL & CHAT ASSISTANT ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_cust'
    port = 9297
    
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--remote-debugging-port={port}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1600,1050',
        f'--user-data-dir={profile_dir}',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        await asyncio.sleep(2)
        r_new = requests.put(f'http://localhost:{port}/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        
        async with websockets.connect(ws_url, max_size=25000000) as ws:
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

            async def eval_js(expr):
                res = await send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
                return res.get('result', {}).get('result', {}).get('value')

            async def take_screenshot(filename):
                shot = await send('Page.captureScreenshot', {'format': 'png'})
                img_data = base64.b64decode(shot['result']['data'])
                filepath = os.path.join(r'd:\KPMG', filename)
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"  --> Saved screenshot: {filename}")

            await send('Page.enable')
            await send('Runtime.enable')
            
            print("1. Navigating to portal...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(5)

            # Check if landing or already on a view
            view_state = await eval_js("""
            (() => {
                const el = document.querySelector('[ng-controller]');
                if (!el) return 'NO_NG_CONTROLLER';
                const scope = angular.element(el).scope();
                const c = scope.c || scope;
                return { currentView: c.currentView, user: c.user };
            })()
            """)
            print("Initial state:", view_state)

            # If on landing or portal select, trigger demo citizen login
            login_js = """
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c || scope;
                c.loadDemoSession();
                scope.$apply();
                return { currentView: c.currentView, user: c.user.name, cases: c.cases.length, stats: c.stats };
            })()
            """
            demo_res = await eval_js(login_js)
            print("Loaded Customer Demo Session:", demo_res)
            await asyncio.sleep(2)

            # 1. Verify Customer Dashboard
            print("\n--- 1. DASHBOARD VIEW ---")
            dash_info = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const title = document.querySelector('.fnx-dash-header, h1, .fnx-user-badge');
                const cards = Array.from(document.querySelectorAll('.fnx-stat-card, .fnx-metric-card, .fnx-kpi-card')).map(c => c.innerText.replace(/\\n/g, ' '));
                const recentCases = Array.from(document.querySelectorAll('.fnx-case-row, table tr')).map(r => r.innerText.replace(/\\n/g, ' '));
                return {
                    mainExists: !!main,
                    mainHeight: main ? main.offsetHeight : 0,
                    title: title ? title.innerText : null,
                    statCards: cards,
                    caseCount: recentCases.length
                };
            })()
            """)
            print("Dashboard Info:", json.dumps(dash_info, indent=2))
            await take_screenshot("customer_dashboard_restored.png")

            # 2. Verify Floating Chat Assistant Button & Panel
            print("\n--- 2. FLOATING CHAT ASSISTANT ---")
            ai_info = await eval_js("""
            (() => {
                const trigger = document.querySelector('.fnx-ai-trigger');
                const widget = document.querySelector('.fnx-ai-widget');
                return {
                    widgetExists: !!widget,
                    triggerExists: !!trigger,
                    triggerVisible: trigger ? (trigger.offsetWidth > 0 && trigger.offsetHeight > 0) : false,
                    triggerText: trigger ? trigger.innerText : null
                };
            })()
            """)
            print("Chat Assistant Trigger:", ai_info)

            # Click Chat Assistant trigger
            print("Opening Chat Assistant Drawer...")
            await eval_js("""
            (() => {
                const trigger = document.querySelector('.fnx-ai-trigger');
                if (trigger) trigger.click();
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c || scope;
                c.showAI = true;
                scope.$apply();
            })()
            """)
            await asyncio.sleep(2)
            
            panel_info = await eval_js("""
            (() => {
                const panel = document.querySelector('.fnx-ai-panel');
                const header = document.querySelector('.fnx-ai-header');
                const messages = Array.from(document.querySelectorAll('.fnx-ai-msg')).map(m => m.innerText.replace(/\\n/g, ' '));
                const chips = Array.from(document.querySelectorAll('.fnx-ai-chip')).map(ch => ch.innerText);
                return {
                    panelExists: !!panel,
                    panelVisible: panel ? (panel.offsetWidth > 0 && panel.offsetHeight > 0) : false,
                    headerText: header ? header.innerText.replace(/\\n/g, ' ') : null,
                    messageCount: messages.length,
                    firstMessage: messages[0] || null,
                    chips: chips
                };
            })()
            """)
            print("Chat Assistant Panel Info:", json.dumps(panel_info, indent=2))
            await take_screenshot("customer_chat_assistant_active.png")

            # Close AI panel so it doesn't obstruct full page views
            await eval_js("""
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c || scope;
                c.showAI = false;
                scope.$apply();
            })()
            """)
            await asyncio.sleep(1)

            # 3. Test Track Cases View
            print("\n--- 3. TRACK CASES VIEW ---")
            await eval_js("""
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c || scope;
                c.navigate('trackCases');
                scope.$apply();
            })()
            """)
            await asyncio.sleep(2)
            track_info = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const trackView = document.querySelector('.fnx-track-cases, .fnx-track-workspace, [ng-if*=\"trackCases\"]');
                const casesList = Array.from(document.querySelectorAll('.fnx-case-item, .fnx-track-card, tr')).map(c => c.innerText.replace(/\\n/g, ' '));
                return {
                    mainHeight: main ? main.offsetHeight : 0,
                    trackViewExists: !!trackView,
                    trackViewInsideMain: main && trackView ? main.contains(trackView) : false,
                    trackViewHeight: trackView ? trackView.offsetHeight : 0,
                    trackViewTop: trackView ? trackView.getBoundingClientRect().top : null,
                    casesFound: casesList.length
                };
            })()
            """)
            print("Track Cases Info:", json.dumps(track_info, indent=2))
            await take_screenshot("customer_track_cases_restored.png")

            # 4. Test Evidence Vault View
            print("\n--- 4. EVIDENCE VAULT VIEW ---")
            await eval_js("""
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c || scope;
                c.navigate('evidenceVault');
                scope.$apply();
            })()
            """)
            await asyncio.sleep(2)
            ev_info = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const evView = document.querySelector('.fnx-vault-workspace, .fnx-evidence-view, [ng-if*=\"evidenceVault\"]');
                return {
                    mainHeight: main ? main.offsetHeight : 0,
                    evViewExists: !!evView,
                    evViewInsideMain: main && evView ? main.contains(evView) : false,
                    evViewHeight: evView ? evView.offsetHeight : 0,
                    evViewTop: evView ? evView.getBoundingClientRect().top : null
                };
            })()
            """)
            print("Evidence Vault Info:", json.dumps(ev_info, indent=2))
            await take_screenshot("customer_evidence_vault_restored.png")

            # 5. Test Help & Support View
            print("\n--- 5. HELP & SUPPORT VIEW ---")
            await eval_js("""
            (() => {
                const el = document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c || scope;
                c.navigate('help');
                scope.$apply();
            })()
            """)
            await asyncio.sleep(2)
            help_info = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const helpView = document.querySelector('.fnx-help-workspace, [ng-if*=\"help\"]');
                return {
                    mainHeight: main ? main.offsetHeight : 0,
                    helpViewExists: !!helpView,
                    helpViewInsideMain: main && helpView ? main.contains(helpView) : false,
                    helpViewHeight: helpView ? helpView.offsetHeight : 0,
                    helpViewTop: helpView ? helpView.getBoundingClientRect().top : null
                };
            })()
            """)
            print("Help & Support Info:", json.dumps(help_info, indent=2))
            await take_screenshot("customer_help_restored.png")

            print("\n=== ALL CHECKS COMPLETED ===")

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(test_customer())
