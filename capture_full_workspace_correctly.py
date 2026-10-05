import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def capture_all():
    print("=== CAPTURING COMPLETE ANALYTICS WORKSPACE SCREENS ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_final_correct'
    port = 9283
    
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
            
            for attempt in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    print(f"   App mounted in {attempt+1}s")
                    break

            print("2. Activating Admin Analytics Workspace...")
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
            print("3. Ingesting live data from ServiceNow REST APIs...")
            await asyncio.sleep(6)

            # Confirm scrollable container
            chk_main = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const el = document.querySelector('.fnx-admin-main-content');
                    return el ? { scrollHeight: el.scrollHeight, clientHeight: el.clientHeight } : null;
                })()
                """,
                'returnByValue': True
            })
            print(".fnx-admin-main-content metrics:", json.dumps(chk_main['result']['result'].get('value'), indent=2))

            async def scroll_main_content(y):
                js_scroll = f"""
                (() => {{
                    const el = document.querySelector('.fnx-admin-main-content');
                    if (el) {{
                        el.scrollTop = {y};
                        return el.scrollTop;
                    }}
                    return -1;
                }})()
                """
                r = await send('Runtime.evaluate', {'expression': js_scroll, 'returnByValue': True})
                await asyncio.sleep(1)
                return r['result']['result'].get('value')

            # 1. Section 1: Overview & KPI Row 1 & 2 & Incident Types & Lifecycle Donut
            print("4. Capturing Section 1 (Header, Global Filters, KPIs, Donut, Horizontal Bars)...")
            await scroll_main_content(0)
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_01_kpi_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("   Saved d:/KPMG/analytics_01_kpi_overview.png")

            # 2. Section 2: Severity, Fraud Trend, Financial Impact, Risk Analytics
            print("5. Capturing Section 2 (Severity, Fraud Trend, Financial Exposure, Risk Distribution)...")
            await scroll_main_content(600)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_02_financial_risk.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("   Saved d:/KPMG/analytics_02_financial_risk.png")

            # 3. Section 3: Investigation Performance & Resolution Performance & Investigator & Partner
            print("6. Capturing Section 3 (Investigation Funnel, Resolution, Investigator Ranked Table, Partners)...")
            await scroll_main_content(1200)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_03_investigator_partner.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("   Saved d:/KPMG/analytics_03_investigator_partner.png")

            # 4. Section 4: Evidence Analytics, SLA, Fraud Syndicate Clusters, Outcomes & Ledger
            print("7. Capturing Section 4 (Evidence, SLA, Syndicate Clusters & Outcomes Ledger)...")
            await scroll_main_content(1800)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_04_clusters_outcomes.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("   Saved d:/KPMG/analytics_04_clusters_outcomes.png")

            # 5. Section 5: Interactive Drilldown Modal
            print("8. Opening Interactive Drilldown Modal on 'Critical' severity...")
            js_drill = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.openAnalyticsDrilldown('Severity: Critical', 'severity', 'Critical');
                scope.$apply();
                return "OPENED";
            })()
            """
            await send('Runtime.evaluate', {'expression': js_drill, 'returnByValue': True})
            await asyncio.sleep(1)
            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_05_interactive_drilldown.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("   Saved d:/KPMG/analytics_05_interactive_drilldown.png")

            print("=== CAPTURE COMPLETE ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(capture_all())
