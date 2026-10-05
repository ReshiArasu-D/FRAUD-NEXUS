import asyncio, subprocess, requests, json, websockets, base64, sys, os

sys.stdout.reconfigure(encoding='utf-8')

async def test_verification_workspace():
    print("=== STARTING VERIFICATION QUEUE WORKSPACE NATURAL E2E TEST ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_verif_natural'
    port = 9270
    
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
        
        async with websockets.connect(ws_url, max_size=25000000) as ws:
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
            await asyncio.sleep(5)

            # Step 1: Click 'Get Started'
            print("2. Clicking 'Get Started' on Landing Page...")
            step1_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Get Started'));
                if (b) { b.click(); return "CLICKED_GET_STARTED"; }
                return "NOT_FOUND";
            })()
            """
            r1 = await send('Runtime.evaluate', {'expression': step1_js, 'returnByValue': True})
            print("Step 1:", r1['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 2: Click 'Enter Investigator Workspace'
            print("3. Clicking 'Enter Investigator Workspace'...")
            step2_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Enter Investigator Workspace') || x.innerText.includes('Investigator'));
                if (b) { b.click(); return "CLICKED_INVESTIGATOR_PORTAL"; }
                return "NOT_FOUND";
            })()
            """
            r2 = await send('Runtime.evaluate', {'expression': step2_js, 'returnByValue': True})
            print("Step 2:", r2['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 3: Click 'Demo Quick Login'
            print("4. Clicking 'Demo Quick Login'...")
            step3_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Demo Quick Login') || x.className.includes('fnx-btn-demo'));
                if (b) { b.click(); return "CLICKED_DEMO_LOGIN"; }
                return "NOT_FOUND";
            })()
            """
            r3 = await send('Runtime.evaluate', {'expression': step3_js, 'returnByValue': True})
            print("Step 3:", r3['result']['result'].get('value'))
            await asyncio.sleep(3)

            # Step 4: Click 'Investigation' in Admin Sidebar
            print("5. Clicking 'Investigation' in Admin Sidebar...")
            step4_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('.fnx-sidebar-item, button'));
                const b = btns.find(x => x.innerText.includes('Investigation'));
                if (b) { b.click(); return "CLICKED_INVESTIGATION_SIDEBAR"; }
                return "NOT_FOUND";
            })()
            """
            r4 = await send('Runtime.evaluate', {'expression': step4_js, 'returnByValue': True})
            print("Step 4:", r4['result']['result'].get('value'))
            await asyncio.sleep(3)

            # Check Overview state
            print("6. Checking Overview View State...")
            ov_check_js = """
            (() => {
                const html = document.body.innerHTML;
                const hasCaseDossier = html.includes('CASE DOSSIER') || html.includes('METRICS BREAKDOWN');
                const hasBPEInOverview = html.includes('Dynamic Byte-Level BPE Tokenizer') && !html.includes('Human Verification Workspace');
                return {
                    hasCaseDossier: hasCaseDossier,
                    hasBPEInOverview: hasBPEInOverview,
                    bodyLength: html.length
                };
            })()
            """
            r_ov = await send('Runtime.evaluate', {'expression': ov_check_js, 'returnByValue': True})
            print("Overview Checks:", r_ov['result']['result'].get('value'))

            # Screenshot 1: Overview
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_01_overview_updated.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Saved d:/KPMG/vw_01_overview_updated.png")

            # Step 5: Click 'Verification Queue' in Left Navigation
            print("7. Clicking 'Verification Queue' in Left Navigation...")
            step5_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('.fnx-lnav-btn, button'));
                const b = btns.find(x => x.innerText.includes('Verification Queue'));
                if (b) { b.click(); return "CLICKED_VERIFICATION_QUEUE"; }
                return "NOT_FOUND";
            })()
            """
            r5 = await send('Runtime.evaluate', {'expression': step5_js, 'returnByValue': True})
            print("Step 5:", r5['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 6: Click 'Reset for Demo' to show pending state
            print("8. Clicking '🔄 Reset for Demo'...")
            step6_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Reset for Demo'));
                if (b) { b.click(); return "CLICKED_RESET_DEMO"; }
                return "NOT_FOUND";
            })()
            """
            r6 = await send('Runtime.evaluate', {'expression': step6_js, 'returnByValue': True})
            print("Step 6:", r6['result']['result'].get('value'))
            await asyncio.sleep(1)

            # Screenshot 2: Verification Queue Pending
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_02_verification_pending.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Saved d:/KPMG/vw_02_verification_pending.png")

            # Step 7: Click '✓ Batch Verify All Pending'
            print("9. Clicking '✓ Batch Verify All Pending'...")
            step7_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(x => x.innerText.includes('Batch Verify All Pending'));
                if (b) { b.click(); return "CLICKED_BATCH_VERIFY"; }
                return "NOT_FOUND";
            })()
            """
            r7 = await send('Runtime.evaluate', {'expression': step7_js, 'returnByValue': True})
            print("Step 7:", r7['result']['result'].get('value'))
            await asyncio.sleep(1)

            # Screenshot 3: Verification Queue Confirmed
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_03_verification_confirmed.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Saved d:/KPMG/vw_03_verification_confirmed.png")

            # Copy to brain artifact directory
            import shutil
            art_dir = r'C:\Users\hp\.gemini\antigravity-ide\brain\59316f90-7827-47e6-86b5-4235fae01a28'
            shutil.copy('d:/KPMG/vw_01_overview_updated.png', os.path.join(art_dir, 'vw_overview_updated.png'))
            shutil.copy('d:/KPMG/vw_02_verification_pending.png', os.path.join(art_dir, 'vw_verification_pending.png'))
            shutil.copy('d:/KPMG/vw_03_verification_confirmed.png', os.path.join(art_dir, 'vw_verification_confirmed.png'))
            print("Screenshots copied to artifact directory.")

            print("=== NATURAL E2E VERIFICATION TEST COMPLETE! ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test_verification_workspace())
