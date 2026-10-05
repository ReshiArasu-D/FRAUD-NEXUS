import asyncio, subprocess, requests, json, websockets, base64, sys, os

sys.stdout.reconfigure(encoding='utf-8')

async def test_analytics_workspace():
    print("=== STARTING FRAUDNEXUS ANALYTICS WORKSPACE E2E TEST ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_analytics_test'
    port = 9272
    
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
            
            print("1. Navigating to https://dev187180.service-now.com/fnx...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            # Wait for app to render
            print("2. Polling for app container...")
            for attempt in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelectorAll("button").length > 0',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    print(f"   App ready after {attempt+1}s")
                    break

            # Step 1: Click 'Get Started'
            print("3. Clicking 'Get Started'...")
            step1_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Get Started'));
                if (b) { b.click(); return "CLICKED_GET_STARTED"; }
                return "NOT_FOUND";
            })()
            """
            r1 = await send('Runtime.evaluate', {'expression': step1_js, 'returnByValue': True})
            print("   Result:", r1['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 2: Click 'Enter Investigator Workspace'
            print("4. Clicking 'Enter Investigator Workspace'...")
            step2_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Enter Investigator Workspace') || x.innerText.includes('Investigator'));
                if (b) { b.click(); return "CLICKED_INVESTIGATOR_PORTAL"; }
                return "NOT_FOUND";
            })()
            """
            r2 = await send('Runtime.evaluate', {'expression': step2_js, 'returnByValue': True})
            print("   Result:", r2['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 3: Click 'Demo Quick Login'
            print("5. Clicking 'Demo Quick Login'...")
            step3_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Demo Quick Login') || x.className.includes('fnx-btn-demo'));
                if (b) { b.click(); return "CLICKED_DEMO_LOGIN"; }
                return "NOT_FOUND";
            })()
            """
            r3 = await send('Runtime.evaluate', {'expression': step3_js, 'returnByValue': True})
            print("   Result:", r3['result']['result'].get('value'))
            await asyncio.sleep(3)

            # Step 4: Click 'Analytics' in Admin Sidebar
            print("6. Clicking 'Analytics' in Admin Sidebar...")
            step4_js = """
            (() => {
                const items = Array.from(document.querySelectorAll('.fnx-sidebar-item, button'));
                const b = items.find(x => x.innerText.trim().startsWith('Analytics'));
                if (b) { b.click(); return "CLICKED_ANALYTICS_SIDEBAR"; }
                return "NOT_FOUND";
            })()
            """
            r4 = await send('Runtime.evaluate', {'expression': step4_js, 'returnByValue': True})
            print("   Result:", r4['result']['result'].get('value'))
            await asyncio.sleep(3)

            # Step 5: Verify Analytics Workspace DOM & Data
            print("7. Inspecting Analytics Workspace DOM...")
            eval_js = """
            (() => {
                const app = document.querySelector('.fnx-app') || document.body;
                const scope = angular.element(app).scope();
                const c = scope ? scope.c : null;
                
                const headerTitle = document.querySelector('.header-title') ? document.querySelector('.header-title').innerText : '';
                const kpis = Array.from(document.querySelectorAll('.kpi-val')).map(x => x.innerText.trim());
                const cards = Array.from(document.querySelectorAll('.chart-title')).map(x => x.innerText.trim());
                const filterCount = document.querySelectorAll('.filter-item').length;
                const drilldownModal = document.querySelector('.fnx-analytics-modal-backdrop') !== null;
                
                return {
                    adminModule: c ? c.adminModule : null,
                    headerTitle: headerTitle,
                    kpiValues: kpis,
                    chartTitles: cards,
                    filterCount: filterCount,
                    totalCasesRaw: c ? c.totalCasesRaw : null,
                    activeFilteredCasesCount: c && c.activeFilteredCases ? c.activeFilteredCases.length : 0,
                    kpiExposure: c && c.analyticsKPIs ? c.analyticsKPIs.totalExposureFormatted : null,
                    kpiRecovered: c && c.analyticsKPIs ? c.analyticsKPIs.recoveredFormatted : null
                };
            })()
            """
            r_eval = await send('Runtime.evaluate', {'expression': eval_js, 'returnByValue': True})
            data = r_eval['result']['result'].get('value')
            print("   Analytics State:", json.dumps(data, indent=2))

            # Screenshot 1: Full top view (Header, Filters, KPIs, Overview Charts)
            print("8. Capturing Top View Screenshot...")
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_01_top_view.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("   Saved d:/KPMG/analytics_01_top_view.png")

            # Scroll down to middle section
            print("9. Scrolling to Financial, Risk & Performance sections...")
            await send('Runtime.evaluate', {'expression': 'window.scrollTo(0, 800)'})
            await asyncio.sleep(1)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_02_middle_view.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("   Saved d:/KPMG/analytics_02_middle_view.png")

            # Scroll down to bottom section (Investigator, Partner, Evidence, Patterns, Outcomes)
            print("10. Scrolling to Investigator, Partner, Evidence, Fraud Clusters & Outcomes...")
            await send('Runtime.evaluate', {'expression': 'window.scrollTo(0, 1600)'})
            await asyncio.sleep(1)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_03_bottom_view.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("   Saved d:/KPMG/analytics_03_bottom_view.png")

            # Step 6: Test Filtering
            print("11. Testing Global Filter interaction (Filter by Severity: Critical)...")
            filter_js = """
            (() => {
                const app = document.querySelector('.fnx-app') || document.body;
                const scope = angular.element(app).scope();
                if (scope && scope.c) {
                    scope.c.analyticsFilters.severity = 'Critical';
                    scope.c.applyAnalyticsFilters();
                    scope.$apply();
                    return {
                        filteredCount: scope.c.filteredCasesCount,
                        kpis: scope.c.analyticsKPIs
                    };
                }
                return "SCOPE_NOT_FOUND";
            })()
            """
            r_filt = await send('Runtime.evaluate', {'expression': filter_js, 'returnByValue': True})
            print("   Filtered result:", json.dumps(r_filt['result']['result'].get('value'), indent=2))
            
            await send('Runtime.evaluate', {'expression': 'window.scrollTo(0, 0)'})
            await asyncio.sleep(1)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_04_filtered_view.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("   Saved d:/KPMG/analytics_04_filtered_view.png")

            # Step 7: Test Drill-Down Modal
            print("12. Testing Drill-Down Modal...")
            drilldown_js = """
            (() => {
                const app = document.querySelector('.fnx-app') || document.body;
                const scope = angular.element(app).scope();
                if (scope && scope.c) {
                    scope.c.openAnalyticsDrilldown('severity', 'Critical');
                    scope.$apply();
                    return {
                        modalOpen: scope.c.showAnalyticsDrilldownModal,
                        casesCount: scope.c.drilldownCases.length,
                        title: scope.c.drilldownTitle
                    };
                }
                return "SCOPE_NOT_FOUND";
            })()
            """
            r_drill = await send('Runtime.evaluate', {'expression': drilldown_js, 'returnByValue': True})
            print("   Drill-down result:", json.dumps(r_drill['result']['result'].get('value'), indent=2))
            await asyncio.sleep(1)

            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/analytics_05_drilldown_modal.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("   Saved d:/KPMG/analytics_05_drilldown_modal.png")

            # Close modal & Reset Filters
            print("13. Closing Modal and Resetting Filters...")
            reset_js = """
            (() => {
                const app = document.querySelector('.fnx-app') || document.body;
                const scope = angular.element(app).scope();
                if (scope && scope.c) {
                    scope.c.closeDrilldownModal();
                    scope.c.resetAnalyticsFilters();
                    scope.$apply();
                    return "RESET_DONE";
                }
                return "SCOPE_NOT_FOUND";
            })()
            """
            await send('Runtime.evaluate', {'expression': reset_js, 'returnByValue': True})
            await asyncio.sleep(1)

            # Step 8: Test Preserved Sidebar items (Investigation & Verification Workspace)
            print("14. Verifying preserved Investigation and Verification modules...")
            verify_nav_js = """
            (() => {
                const items = Array.from(document.querySelectorAll('.fnx-sidebar-item, button'));
                const invBtn = items.find(x => x.innerText.trim().startsWith('Investigation'));
                const vwBtn = items.find(x => x.innerText.trim().startsWith('Verification Workspace'));
                return {
                    hasInvestigation: invBtn !== undefined,
                    hasVerificationWorkspace: vwBtn !== undefined
                };
            })()
            """
            r_nav = await send('Runtime.evaluate', {'expression': verify_nav_js, 'returnByValue': True})
            print("   Sidebar Integrity:", r_nav['result']['result'].get('value'))

            print("=== ANALYTICS WORKSPACE E2E TEST COMPLETED SUCCESSFULLY ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test_analytics_workspace())
