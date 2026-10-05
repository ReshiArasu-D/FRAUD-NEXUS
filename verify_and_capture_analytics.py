import asyncio, subprocess, requests, json, websockets, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

async def verify_and_capture_analytics():
    print("=== CAPTURING REAL ANALYTICS WORKSPACE SCREENSHOTS ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_verify_cap'
    port = 9277
    
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
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # Switch view to adminWorkspace and module to analytics
            print("2. Switching to Admin Analytics Module...")
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

            # Wait for data fetch and angular digest
            print("3. Waiting for ServiceNow REST data ingestion & aggregation...")
            await asyncio.sleep(6)

            # Inspect state
            js_inspect = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                return {
                    module: c.adminModule,
                    casesLoaded: c.rawCasesList ? c.rawCasesList.length : 0,
                    kpis: c.analyticsKPIs,
                    typeBars: c.analyticsTypeBars ? c.analyticsTypeBars.length : 0,
                    statuses: c.analyticsStatusList ? c.analyticsStatusList.length : 0,
                    severities: c.analyticsSeverityList ? c.analyticsSeverityList.length : 0,
                    trendPath: c.analyticsTrendLinePath ? c.analyticsTrendLinePath.substring(0, 30) : '',
                    investigators: c.analyticsInvestigatorList ? c.analyticsInvestigatorList.length : 0,
                    partners: c.analyticsPartnerList ? c.analyticsPartnerList.length : 0,
                    clusters: c.analyticsClustersList ? c.analyticsClustersList.length : 0
                };
            })()
            """
            r_ins = await send('Runtime.evaluate', {'expression': js_inspect, 'returnByValue': True})
            print("Aggregated State:", json.dumps(r_ins['result']['result'].get('value'), indent=2))

            # Capture View 1: Top section (KPIs, Incident Types, Status Donut, Severity, Trend)
            print("4. Capturing Screenshot 1 (Top Section)...")
            await send('Runtime.evaluate', {'expression': 'window.scrollTo(0, 0)'})
            await asyncio.sleep(1)
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_01_top_populated.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("   Saved d:/KPMG/analytics_01_top_populated.png")

            # Capture View 2: Middle section (Financial Exposure, Risk, Investigation Stages, Resolution)
            print("5. Capturing Screenshot 2 (Middle Section)...")
            await send('Runtime.evaluate', {'expression': 'window.scrollTo(0, 680)'})
            await asyncio.sleep(1)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_02_middle_populated.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("   Saved d:/KPMG/analytics_02_middle_populated.png")

            # Capture View 3: Lower section (Investigator, Partner, Evidence, SLA)
            print("6. Capturing Screenshot 3 (Lower Section)...")
            await send('Runtime.evaluate', {'expression': 'window.scrollTo(0, 1350)'})
            await asyncio.sleep(1)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_03_lower_populated.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("   Saved d:/KPMG/analytics_03_lower_populated.png")

            # Capture View 4: Bottom section (Fraud Patterns/Clusters, Case Outcomes, Recovery Ledger)
            print("7. Capturing Screenshot 4 (Bottom Section)...")
            await send('Runtime.evaluate', {'expression': 'window.scrollTo(0, 2050)'})
            await asyncio.sleep(1)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_04_bottom_populated.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("   Saved d:/KPMG/analytics_04_bottom_populated.png")

            # Test Drilldown Modal on 'Payment Fraud'
            print("8. Opening Drilldown Modal for Payment Fraud...")
            drill_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.openAnalyticsDrilldown('Incident Type: Payment Fraud', 'type', 'Payment Fraud');
                scope.$apply();
                return {
                    modalOpen: scope.c.showAnalyticsDrilldownModal,
                    casesCount: scope.c.drilldownCases.length,
                    title: scope.c.drilldownTitle
                };
            })()
            """
            r_drill = await send('Runtime.evaluate', {'expression': drill_js, 'returnByValue': True})
            print("   Drilldown Info:", json.dumps(r_drill['result']['result'].get('value'), indent=2))
            await asyncio.sleep(1)
            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_05_drilldown_populated.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("   Saved d:/KPMG/analytics_05_drilldown_populated.png")

            # Close Modal
            await send('Runtime.evaluate', {'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.closeDrilldownModal(); angular.element(document.querySelector(".fnx-app")).scope().$apply();'})
            await asyncio.sleep(1)

            # Test Navigation to Investigation & Verification Workspace
            print("9. Testing preserved modules navigation...")
            nav_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                
                // Go to investigation
                c.setAdminModule('investigation');
                scope.$apply();
                const invOk = (c.adminModule === 'investigation');
                
                // Go to verification workspace
                c.setAdminModule('intelligence');
                scope.$apply();
                const vwOk = (c.adminModule === 'intelligence');
                
                // Return to analytics
                c.setAdminModule('analytics');
                scope.$apply();
                const anOk = (c.adminModule === 'analytics');
                
                return {
                    investigationIntact: invOk,
                    verificationWorkspaceIntact: vwOk,
                    analyticsIntact: anOk
                };
            })()
            """
            r_nav = await send('Runtime.evaluate', {'expression': nav_js, 'returnByValue': True})
            print("   Navigation Integrity:", json.dumps(r_nav['result']['result'].get('value'), indent=2))

            print("=== VERIFICATION & SCREENSHOT CAPTURE COMPLETE ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(verify_and_capture_analytics())
