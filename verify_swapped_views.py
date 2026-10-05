import asyncio, subprocess, requests, json, websockets, base64, sys, os, shutil

sys.stdout.reconfigure(encoding='utf-8')

async def test_swapped():
    print("=== TESTING RESTORED INVESTIGATION & WIRED VERIFICATION WORKSPACE ===")
    port = 9310
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--remote-debugging-port={port}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1600,1050',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile_swap_wait',
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
            print("1. Loading https://dev187180.service-now.com/fnx...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})

            # Wait up to 30 seconds for .fnx-app to appear
            print("Waiting for .fnx-app to load...")
            for i in range(30):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': '!!document.querySelector(".fnx-app")',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    print(f"Page loaded in {i+1} seconds!")
                    break

            await asyncio.sleep(2)

            # 1. Switch to Investigation module (should be restored original)
            print("2. Testing Restored Investigation Module...")
            res_inv = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const el = document.querySelector('.fnx-app');
                    if (!el) return { error: '.fnx-app not found' };
                    const scope = angular.element(el).scope();
                    const c = scope.c;
                    c.currentView = 'adminWorkspace';
                    c.adminModule = 'investigation';
                    c.investigationTab = 'overview';
                    scope.$apply();
                    
                    const html = document.body.innerHTML;
                    return {
                        success: true,
                        adminModule: c.adminModule,
                        hasActiveInvestigations: html.includes('ACTIVE INVESTIGATIONS'),
                        hasOriginalActions: html.includes('Assign') && html.includes('Add Task'),
                        hasStatutoryCompliance: html.includes('STATUTORY COMPLIANCE'),
                        hasOverviewTab: html.includes('Incident Details')
                    };
                })()
                """,
                'returnByValue': True
            })
            val_inv = res_inv['result']['result'].get('value')
            print("1. Restored Investigation Module:", val_inv)
            await asyncio.sleep(2)

            # Screenshot of original investigation module
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/swapped_01_original_investigation.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Saved d:/KPMG/swapped_01_original_investigation.png")

            # 2. Switch to Verification Workspace module (c.adminModule = 'intelligence')
            print("3. Testing Wired Verification Workspace Module...")
            res_vw = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const el = document.querySelector('.fnx-app');
                    const scope = angular.element(el).scope();
                    const c = scope.c;
                    c.setAdminModule('intelligence');
                    scope.$apply();

                    const html = document.body.innerHTML;
                    return {
                        success: true,
                        adminModule: c.adminModule,
                        hasCaseHeader: html.includes('FNX-2026-00847'),
                        has16Domains: html.includes('INVESTIGATION DOMAINS'),
                        hasGenAIModalBtn: html.includes('Generative Intelligence'),
                        hasRiskDial: html.includes('RISK EVALUATION'),
                        hasVerificationQueueTab: html.includes('Verification Queue')
                    };
                })()
                """,
                'returnByValue': True
            })
            val_vw = res_vw['result']['result'].get('value')
            print("2. Wired Verification Workspace Module:", val_vw)
            await asyncio.sleep(2)

            # Screenshot of Verification Workspace
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/swapped_02_verification_workspace.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Saved d:/KPMG/swapped_02_verification_workspace.png")

            # Copy to brain artifact directory
            art_dir = r'C:\Users\hp\.gemini\antigravity-ide\brain\59316f90-7827-47e6-86b5-4235fae01a28'
            shutil.copy('d:/KPMG/swapped_01_original_investigation.png', os.path.join(art_dir, 'swapped_01_original_investigation.png'))
            shutil.copy('d:/KPMG/swapped_02_verification_workspace.png', os.path.join(art_dir, 'swapped_02_verification_workspace.png'))
            print("Screenshots copied to brain artifacts directory.")
            print("=== VERIFICATION COMPLETE ===")
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test_swapped())
