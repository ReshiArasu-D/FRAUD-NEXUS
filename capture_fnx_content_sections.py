import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def capture_fnx_sections():
    print("=== CAPTURING ALL SECTIONS VIA .fnx-content.scrollTop ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_scroll_fnx'
    port = 9279
    
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

            # Switch view to adminWorkspace and module to analytics
            print("Switching to Admin Analytics Module...")
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

            # Check height of .fnx-content
            chk_h = await send('Runtime.evaluate', {
                'expression': '(() => { const c = document.querySelector(".fnx-content"); return c ? { scrollHeight: c.scrollHeight, clientHeight: c.clientHeight } : null; })()',
                'returnByValue': True
            })
            print(".fnx-content geometry:", json.dumps(chk_h['result']['result'].get('value'), indent=2))

            async def scroll_to(y):
                s_js = f"""
                (() => {{
                    const el = document.querySelector('.fnx-content');
                    if (el) {{
                        el.scrollTop = {y};
                    }}
                }})()
                """
                await send('Runtime.evaluate', {'expression': s_js})
                await asyncio.sleep(1)

            # 1. Top Section (KPIs, Incident Types, Status Donut)
            await scroll_to(0)
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/sec_01_kpi_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Captured sec_01_kpi_overview.png")

            # 2. Severity & Fraud Trend & Financial Exposure
            await scroll_to(650)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/sec_02_trend_financial_risk.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Captured sec_02_trend_financial_risk.png")

            # 3. Investigation Stages Funnel & Resolution Performance
            await scroll_to(1300)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/sec_03_investigation_resolution.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Captured sec_03_investigation_resolution.png")

            # 4. Investigator Performance & Partner Analytics
            await scroll_to(1950)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/sec_04_investigator_partner.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("Captured sec_04_investigator_partner.png")

            # 5. Evidence Analytics & SLA / Alerts
            await scroll_to(2600)
            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/sec_05_evidence_sla.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("Captured sec_05_evidence_sla.png")

            # 6. Fraud Patterns & Potential Syndicate Clusters
            await scroll_to(3250)
            scr6 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/sec_06_fraud_patterns_clusters.png', 'wb') as f:
                f.write(base64.b64decode(scr6['result']['data']))
            print("Captured sec_06_fraud_patterns_clusters.png")

            # 7. Case Outcomes & Financial Reconciliation Ledger
            await scroll_to(3900)
            scr7 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/sec_07_outcomes_ledger.png', 'wb') as f:
                f.write(base64.b64decode(scr7['result']['data']))
            print("Captured sec_07_outcomes_ledger.png")

            print("=== ALL SECTIONS CAPTURED SUCCESSFULLY ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(capture_fnx_sections())
