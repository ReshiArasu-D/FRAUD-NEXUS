import asyncio, subprocess, requests, json, websockets, base64, sys, os, shutil

sys.stdout.reconfigure(encoding='utf-8')

async def test_scope():
    port = 9292
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--remote-debugging-port={port}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1600,1050',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile_fnx_app',
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
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(5)

            # Test accessing scope on .fnx-app
            res = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const el = document.querySelector('.fnx-app');
                    if (!el) return { error: '.fnx-app element not found' };
                    const scope = angular.element(el).scope();
                    if (!scope || !scope.c) return { error: 'scope.c not found on .fnx-app' };
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
                        caseNum: c.activeInvestigationCase.number
                    };
                })()
                """,
                'returnByValue': True
            })
            print("Scope Test Result:", res['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Check if Overview card is visible
            res_ov = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const html = document.body.innerHTML;
                    return {
                        hasDossier: html.includes('CASE DOSSIER &amp; METRICS BREAKDOWN') || html.includes('CASE DOSSIER & METRICS BREAKDOWN'),
                        hasOldBPEInOverview: html.includes('Dynamic Byte-Level BPE Tokenizer')
                    };
                })()
                """,
                'returnByValue': True
            })
            print("Overview check:", res_ov['result']['result'].get('value'))

            # Screenshot 1: Overview
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_01_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Saved d:/KPMG/vw_live_01_overview.png")

            # Switch to Verification Queue
            res_vq = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const el = document.querySelector('.fnx-app');
                    const scope = angular.element(el).scope();
                    const c = scope.c;
                    c.setInvestigationTab('verification');
                    c.resetVerificationQueue();
                    scope.$apply();
                    return {
                        tab: c.investigationTab,
                        pendingCount: c.getPendingVerificationCount()
                    };
                })()
                """,
                'returnByValue': True
            })
            print("Verification Queue (Pending):", res_vq['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Screenshot 2: Verification Queue Pending
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_02_verif_pending.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Saved d:/KPMG/vw_live_02_verif_pending.png")

            # Batch Verify
            res_bv = await send('Runtime.evaluate', {
                'expression': """
                (() => {
                    const el = document.querySelector('.fnx-app');
                    const scope = angular.element(el).scope();
                    const c = scope.c;
                    c.confirmAllPending();
                    scope.$apply();
                    return {
                        tab: c.investigationTab,
                        pendingCount: c.getPendingVerificationCount()
                    };
                })()
                """,
                'returnByValue': True
            })
            print("Verification Queue (Confirmed):", res_bv['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Screenshot 3: Verification Queue Confirmed
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_03_verif_confirmed.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Saved d:/KPMG/vw_live_03_verif_confirmed.png")

            # Copy to brain artifact directory
            art_dir = r'C:\Users\hp\.gemini\antigravity-ide\brain\59316f90-7827-47e6-86b5-4235fae01a28'
            shutil.copy('d:/KPMG/vw_live_01_overview.png', os.path.join(art_dir, 'vw_live_01_overview.png'))
            shutil.copy('d:/KPMG/vw_live_02_verif_pending.png', os.path.join(art_dir, 'vw_live_02_verif_pending.png'))
            shutil.copy('d:/KPMG/vw_live_03_verif_confirmed.png', os.path.join(art_dir, 'vw_live_03_verif_confirmed.png'))
            print("All screenshots successfully copied to artifact directory.")
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test_scope())
