import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def capture_all_sections():
    profile_dir = r'd:\KPMG\.edge_temp_profile_scroll_test'
    port = 9278
    
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

            js_switch = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                c.currentView = 'adminWorkspace';
                c.setAdminModule('analytics');
                scope.$apply();
                return "READY";
            })()
            """
            await send('Runtime.evaluate', {'expression': js_switch, 'returnByValue': True})
            await asyncio.sleep(6)

            # Find scrollable parent
            find_scroll_js = """
            (() => {
                let el = document.querySelector('.fnx-analytics-workspace');
                let scrollables = [];
                while (el) {
                    if (el.scrollHeight > el.clientHeight) {
                        scrollables.push({
                            tag: el.tagName,
                            className: el.className,
                            scrollHeight: el.scrollHeight,
                            clientHeight: el.clientHeight
                        });
                    }
                    el = el.parentElement;
                }
                return scrollables;
            })()
            """
            r_scroll = await send('Runtime.evaluate', {'expression': find_scroll_js, 'returnByValue': True})
            print("Scrollable parents:", json.dumps(r_scroll['result']['result'].get('value'), indent=2))

            # Helper to scroll
            async def scroll_elem(y):
                s_js = f"""
                (() => {{
                    const el = document.querySelector('.fnx-admin-main') || document.querySelector('.fnx-analytics-workspace') || window;
                    if (el.scrollTo) el.scrollTo(0, {y});
                    window.scrollTo(0, {y});
                    document.documentElement.scrollTop = {y};
                    document.body.scrollTop = {y};
                }})()
                """
                await send('Runtime.evaluate', {'expression': s_js})
                await asyncio.sleep(1)

            # Section 1: Top (KPIs, Incident Types, Status Donut)
            await scroll_elem(0)
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_sec_01_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Captured section 1: Overview")

            # Section 2: Severity, Fraud Trend, Financial Impact, Risk Analytics
            await scroll_elem(550)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_sec_02_financial_risk.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Captured section 2: Financial & Risk")

            # Section 3: Investigation Performance & Resolution Performance
            await scroll_elem(1150)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_sec_03_investigation_resolution.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Captured section 3: Investigation Performance")

            # Section 4: Investigator Performance & Partner Analytics
            await scroll_elem(1750)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_sec_04_investigator_partner.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("Captured section 4: Investigator & Partner")

            # Section 5: Evidence Analytics & SLA / Alerts
            await scroll_elem(2350)
            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_sec_05_evidence_sla.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("Captured section 5: Evidence & SLA")

            # Section 6: Fraud Patterns & Potential Syndicate Clusters
            await scroll_elem(2950)
            scr6 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_sec_06_fraud_patterns.png', 'wb') as f:
                f.write(base64.b64decode(scr6['result']['data']))
            print("Captured section 6: Fraud Patterns")

            # Section 7: Case Outcomes & Financial Reconciliation Ledger
            await scroll_elem(3550)
            scr7 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_sec_07_outcomes_ledger.png', 'wb') as f:
                f.write(base64.b64decode(scr7['result']['data']))
            print("Captured section 7: Case Outcomes & Ledger")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(capture_all_sections())
