import asyncio, subprocess, requests, json, websockets, base64, sys, os

sys.stdout.reconfigure(encoding='utf-8')

async def run_e2e_test():
    print("=== STARTING FRAUDNEXUS VERIFICATION WORKSPACE E2E TEST (WITH .fnx-app) ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_vw_e2e2'
    port = 9261
    
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
        
        async with websockets.connect(ws_url, max_size=20000000) as ws:
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
            await asyncio.sleep(6)

            # Access Admin Portal
            print("2. Switching to Admin Verification Workspace...")
            login_js = """
            (() => {
                const el = document.querySelector(".fnx-app");
                if (!el) return { error: ".fnx-app element not found" };
                const scope = angular.element(el).scope();
                if (!scope || !scope.c) return { error: "Angular scope not found on .fnx-app" };
                const c = scope.c;
                
                c.currentView = 'adminWorkspace';
                c.adminModule = 'investigation';
                c.investigationTab = 'overview';
                if (!c.activeInvestigationCase) {
                    c.activeInvestigationCase = c.setupDefaultInvestigationCase();
                }
                scope.$apply();
                return {
                    success: true,
                    currentView: c.currentView,
                    adminModule: c.adminModule,
                    investigationTab: c.investigationTab,
                    caseNumber: c.activeInvestigationCase ? c.activeInvestigationCase.number : null,
                    evidenceCount: c.activeInvestigationCase ? c.activeInvestigationCase.evidence.length : 0,
                    findingsCount: c.activeInvestigationCase ? c.activeInvestigationCase.findings.length : 0
                };
            })()
            """
            res_login = await send('Runtime.evaluate', {'expression': login_js, 'returnByValue': True})
            print("Login State:", res_login['result']['result'].get('value', {}))
            await asyncio.sleep(2)

            # 1. Screenshot: Overview
            print("3. Capturing Screenshot: Verification Workspace Overview...")
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_01_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Saved vw_01_overview.png")

            # 2. Screenshot: Evidence
            print("4. Testing Evidence Workspace...")
            await send('Runtime.evaluate', {
                'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.setInvestigationTab("evidence"); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_02_evidence.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Saved vw_02_evidence.png")

            # 3. Screenshot: Cyber Attack Chain
            print("5. Testing Cyber Analysis & Attack Chain...")
            await send('Runtime.evaluate', {
                'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.setInvestigationTab("cyber"); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_03_cyber_chain.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Saved vw_03_cyber_chain.png")

            # 4. Screenshot: Partner Requests
            print("6. Testing Partner Requests View...")
            await send('Runtime.evaluate', {
                'expression': 'angular.element(document.querySelector(".fnx-app")).scope().c.setInvestigationTab("partnerRequests"); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_04_partner_requests.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("Saved vw_04_partner_requests.png")

            # 5. Screenshot: Generative Intelligence Modal
            print("7. Testing Generative Intelligence Modal...")
            await send('Runtime.evaluate', {
                'expression': 'const c = angular.element(document.querySelector(".fnx-app")).scope().c; c.openGenAIModal(); c.selectedGenAIMode = "journey"; c.generateSelectedIntelligence(); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(2)
            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_05_genai_modal.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("Saved vw_05_genai_modal.png")

            # 6. Screenshot: Human Decision & Resolution
            print("8. Testing Human Decision Area & Manager Approval...")
            await send('Runtime.evaluate', {
                'expression': 'const c = angular.element(document.querySelector(".fnx-app")).scope().c; c.showGenAIModal = false; c.setInvestigationTab("decision"); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            scr6 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_06_human_decision.png', 'wb') as f:
                f.write(base64.b64decode(scr6['result']['data']))
            print("Saved vw_06_human_decision.png")

            # 7. Screenshot: Internal Admin Report
            print("9. Testing Case Reports (Admin)...")
            await send('Runtime.evaluate', {
                'expression': 'const c = angular.element(document.querySelector(".fnx-app")).scope().c; c.setInvestigationTab("report"); c.reportSubTab = "admin"; angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            scr7 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_07_admin_report.png', 'wb') as f:
                f.write(base64.b64decode(scr7['result']['data']))
            print("Saved vw_07_admin_report.png")

            # 8. Screenshot: Customer Safe Report
            print("10. Testing Customer-Facing Safe Report...")
            await send('Runtime.evaluate', {
                'expression': 'const c = angular.element(document.querySelector(".fnx-app")).scope().c; c.reportSubTab = "customer"; angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            scr8 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_08_customer_report.png', 'wb') as f:
                f.write(base64.b64decode(scr8['result']['data']))
            print("Saved vw_08_customer_report.png")

            # 9. Screenshot: Demo Walkthrough Banner
            print("11. Testing Demo Walkthrough Banner...")
            await send('Runtime.evaluate', {
                'expression': 'const c = angular.element(document.querySelector(".fnx-app")).scope().c; c.runEndToEndDemo(); angular.element(document.querySelector(".fnx-app")).scope().$apply();'
            })
            await asyncio.sleep(1)
            scr9 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_09_demo_walkthrough.png', 'wb') as f:
                f.write(base64.b64decode(scr9['result']['data']))
            print("Saved vw_09_demo_walkthrough.png")

            print("\n🎉 ALL E2E STEPS WITH .fnx-app EXECUTED AND CAPTURED!")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(run_e2e_test())
