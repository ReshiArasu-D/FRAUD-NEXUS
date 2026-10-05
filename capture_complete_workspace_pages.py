import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def capture_complete():
    print("=== CAPTURING FULL-LENGTH ANALYTICS WORKSPACE SECTIONS ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_final_cap'
    port = 9281
    
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

            print("2. Entering Analytics Workspace...")
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

            async def scroll_main(y):
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

            # Section 1: Overview & KPI Row 1 & 2 & Donut / Horizontal Bars
            print("3. Capturing Viewport 1 (Top / KPIs / Breakdown)...")
            await scroll_main(0)
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_view_1_overview_kpis.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("   Saved analytics_view_1_overview_kpis.png")

            # Section 2: Severity, Fraud Trend, Financial Impact, Risk Analytics
            print("4. Capturing Viewport 2 (Financial Impact & Risk)...")
            await scroll_main(580)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_view_2_financial_risk.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("   Saved analytics_view_2_financial_risk.png")

            # Section 3: Investigation Performance & Resolution & Investigator & Partner
            print("5. Capturing Viewport 3 (Investigation, Investigator & Partner)...")
            await scroll_main(1250)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_view_3_investigator_partner.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("   Saved analytics_view_3_investigator_partner.png")

            # Section 4: Evidence, SLA, Fraud Patterns / Clusters & Outcomes
            print("6. Capturing Viewport 4 (Evidence, SLA, Syndicate Clusters & Outcomes)...")
            await scroll_main(1950)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_view_4_clusters_outcomes.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("   Saved analytics_view_4_clusters_outcomes.png")

            # Section 5: Interactive Drilldown Modal
            print("7. Opening Interactive Drilldown Modal for High Risk Cases...")
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
            with open('d:/KPMG/analytics_view_5_interactive_drilldown.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("   Saved analytics_view_5_interactive_drilldown.png")

            print("=== ALL ANALYTICS WORKSPACE SCREENSHOTS CAPTURED ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(capture_complete())
