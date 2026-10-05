import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def natural_capture():
    print("=== NATURAL USER FLOW CAPTURE ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_natural_full'
    port = 9282
    
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

            print("1. Navigating to portal...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelectorAll("button").length > 0',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # 1. Click Get Started
            print("2. Clicking 'Get Started'...")
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(x => x.innerText.includes("Get Started")).click()'
            })
            await asyncio.sleep(2)

            # 2. Click Enter Investigator Workspace
            print("3. Clicking 'Enter Investigator Workspace'...")
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(x => x.innerText.includes("Investigator")).click()'
            })
            await asyncio.sleep(2)

            # 3. Click Demo Quick Login
            print("4. Clicking 'Demo Quick Login'...")
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(x => x.innerText.includes("Demo Quick Login") || x.className.includes("fnx-btn-demo")).click()'
            })
            await asyncio.sleep(3)

            # 4. Click Analytics in Admin Sidebar
            print("5. Clicking 'Analytics' in Admin Sidebar...")
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll(".fnx-sidebar-item")).find(x => x.innerText.includes("Analytics")).click()'
            })
            
            # Wait for data fetch
            print("6. Waiting for analytics aggregation...")
            await asyncio.sleep(6)

            # Check scroll container
            scroll_info = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const el = document.querySelector('.fnx-admin-main-content');
                    return el ? { scrollHeight: el.scrollHeight, clientHeight: el.clientHeight } : null;
                })()
                """,
                'returnByValue': True
            })
            print(".fnx-admin-main-content info:", json.dumps(scroll_info['result']['result'].get('value'), indent=2))

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

            # 1. Section 1: Overview & KPI Row 1 & 2 & Donut / Horizontal Bars
            print("7. Capturing Viewport 1 (Top / KPIs / Breakdown)...")
            await scroll_main(0)
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/final_analytics_view_1_overview_kpis.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("   Saved final_analytics_view_1_overview_kpis.png")

            # 2. Section 2: Severity, Fraud Trend, Financial Impact, Risk Analytics
            print("8. Capturing Viewport 2 (Financial Impact & Risk)...")
            await scroll_main(580)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/final_analytics_view_2_financial_risk.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("   Saved final_analytics_view_2_financial_risk.png")

            # 3. Section 3: Investigation Performance & Resolution & Investigator & Partner
            print("9. Capturing Viewport 3 (Investigation, Investigator & Partner)...")
            await scroll_main(1250)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/final_analytics_view_3_investigator_partner.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("   Saved final_analytics_view_3_investigator_partner.png")

            # 4. Section 4: Evidence, SLA, Fraud Patterns / Clusters & Outcomes
            print("10. Capturing Viewport 4 (Evidence, SLA, Syndicate Clusters & Outcomes)...")
            await scroll_main(1950)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/final_analytics_view_4_clusters_outcomes.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("   Saved final_analytics_view_4_clusters_outcomes.png")

            # 5. Section 5: Interactive Drilldown Modal
            print("11. Opening Interactive Drilldown Modal for High Risk Cases...")
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
            with open('d:/KPMG/final_analytics_view_5_interactive_drilldown.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("   Saved final_analytics_view_5_interactive_drilldown.png")

            print("=== NATURAL FLOW WORKSPACE SCREENSHOTS CAPTURED ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(natural_capture())
