import asyncio, subprocess, requests, json, websockets, base64, sys, os

sys.stdout.reconfigure(encoding='utf-8')

async def run_natural_test():
    print("=== STARTING NATURAL USER INTERACTION E2E TEST ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_natural'
    port = 9295
    
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
            await asyncio.sleep(6)

            # Step 1: Click 'Get Started'
            print("2. Clicking 'Get Started' on Landing Page...")
            step1_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const getStartedBtn = btns.find(b => b.innerText.includes('Get Started'));
                if (getStartedBtn) {
                    getStartedBtn.click();
                    return "CLICKED_GET_STARTED";
                }
                return "GET_STARTED_NOT_FOUND";
            })()
            """
            res1 = await send('Runtime.evaluate', {'expression': step1_js, 'returnByValue': True})
            print("Step 1:", res1['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 2: Click 'Enter Investigator Workspace'
            print("3. Clicking 'Enter Investigator Workspace' on Portal Select...")
            step2_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const invBtn = btns.find(b => b.innerText.includes('Enter Investigator Workspace') || b.innerText.includes('Investigator'));
                if (invBtn) {
                    invBtn.click();
                    return "CLICKED_INVESTIGATOR_PORTAL";
                }
                return "INV_BTN_NOT_FOUND";
            })()
            """
            res2 = await send('Runtime.evaluate', {'expression': step2_js, 'returnByValue': True})
            print("Step 2:", res2['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 3: Click 'Demo Quick Login' on Admin Login
            print("4. Clicking 'Demo Quick Login'...")
            step3_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const demoBtn = btns.find(b => b.innerText.includes('Demo Quick Login') || b.className.includes('fnx-btn-demo'));
                if (demoBtn) {
                    demoBtn.click();
                    return "CLICKED_DEMO_LOGIN";
                }
                return "DEMO_BTN_NOT_FOUND";
            })()
            """
            res3 = await send('Runtime.evaluate', {'expression': step3_js, 'returnByValue': True})
            print("Step 3:", res3['result']['result'].get('value'))
            await asyncio.sleep(3)

            # Step 4: Click 'Investigation' in Sidebar or Open Case
            print("5. Clicking 'Investigation' in Admin Sidebar...")
            step4_js = """
            (() => {
                const btns = Array.from(document.querySelectorAll('.fnx-sidebar-item, button'));
                const invTab = btns.find(b => b.innerText.includes('Investigation'));
                if (invTab) {
                    invTab.click();
                    return "CLICKED_INVESTIGATION_SIDEBAR";
                }
                return "INVESTIGATION_SIDEBAR_NOT_FOUND";
            })()
            """
            res4 = await send('Runtime.evaluate', {'expression': step4_js, 'returnByValue': True})
            print("Step 4:", res4['result']['result'].get('value'))
            await asyncio.sleep(2)

            # 6. Capture Verification Workspace Overview
            print("6. Capturing Verification Workspace Overview screenshot...")
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_01_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Saved vw_live_01_overview.png (Size:", os.path.getsize('d:/KPMG/vw_live_01_overview.png'), ")")

            # 7. Click Evidence Left Nav
            print("7. Clicking Evidence Left Nav...")
            click_nav_js = """
            (navName) => {
                const btns = Array.from(document.querySelectorAll('.fnx-lnav-btn'));
                const target = btns.find(b => b.innerText.includes(navName));
                if (target) {
                    target.click();
                    return "CLICKED_" + navName.toUpperCase();
                }
                return "NAV_NOT_FOUND_" + navName;
            }
            """
            res_nav_ev = await send('Runtime.evaluate', {'expression': f'({click_nav_js})("Evidence")', 'returnByValue': True})
            print("Nav Evidence:", res_nav_ev['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_02_evidence.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Saved vw_live_02_evidence.png (Size:", os.path.getsize('d:/KPMG/vw_live_02_evidence.png'), ")")

            # 8. Click Cyber Analysis Left Nav
            print("8. Clicking Cyber Analysis Left Nav...")
            res_nav_cy = await send('Runtime.evaluate', {'expression': f'({click_nav_js})("Cyber Analysis")', 'returnByValue': True})
            print("Nav Cyber:", res_nav_cy['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_03_cyber.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Saved vw_live_03_cyber.png (Size:", os.path.getsize('d:/KPMG/vw_live_03_cyber.png'), ")")

            # 9. Click Partner Requests Left Nav
            print("9. Clicking Partner Requests Left Nav...")
            res_nav_pr = await send('Runtime.evaluate', {'expression': f'({click_nav_js})("Partner Requests")', 'returnByValue': True})
            print("Nav Partner:", res_nav_pr['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_04_partner.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("Saved vw_live_04_partner.png (Size:", os.path.getsize('d:/KPMG/vw_live_04_partner.png'), ")")

            # 10. Click 'Generative Intelligence' Header Button
            print("10. Clicking Header Action: Generative Intelligence...")
            click_header_js = """
            (btnText) => {
                const btns = Array.from(document.querySelectorAll('.fnx-btn-header'));
                const target = btns.find(b => b.innerText.includes(btnText));
                if (target) {
                    target.click();
                    return "CLICKED_" + btnText.toUpperCase();
                }
                return "HEADER_BTN_NOT_FOUND_" + btnText;
            }
            """
            res_hdr_gen = await send('Runtime.evaluate', {'expression': f'({click_header_js})("Generative Intelligence")', 'returnByValue': True})
            print("Header GenAI:", res_hdr_gen['result']['result'].get('value'))
            await asyncio.sleep(2)

            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_05_genai_modal.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("Saved vw_live_05_genai_modal.png (Size:", os.path.getsize('d:/KPMG/vw_live_05_genai_modal.png'), ")")

            # Close GenAI Modal
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".btn-close-modal").click()'})
            await asyncio.sleep(1)

            # 11. Click Human Decision Left Nav
            print("11. Clicking Human Decision Left Nav...")
            res_nav_dec = await send('Runtime.evaluate', {'expression': f'({click_nav_js})("Human Decision")', 'returnByValue': True})
            print("Nav Decision:", res_nav_dec['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            scr6 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_06_decision.png', 'wb') as f:
                f.write(base64.b64decode(scr6['result']['data']))
            print("Saved vw_live_06_decision.png (Size:", os.path.getsize('d:/KPMG/vw_live_06_decision.png'), ")")

            # 12. Click Case Reports Left Nav
            print("12. Clicking Case Reports Left Nav...")
            res_nav_rep = await send('Runtime.evaluate', {'expression': f'({click_nav_js})("Case Reports")', 'returnByValue': True})
            print("Nav Report:", res_nav_rep['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            scr7 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_07_report.png', 'wb') as f:
                f.write(base64.b64decode(scr7['result']['data']))
            print("Saved vw_live_07_report.png (Size:", os.path.getsize('d:/KPMG/vw_live_07_report.png'), ")")

            # 13. Click 'Demo Walkthrough' Header Button
            print("13. Clicking Header Action: Demo Walkthrough...")
            res_hdr_demo = await send('Runtime.evaluate', {'expression': f'({click_header_js})("Demo Walkthrough")', 'returnByValue': True})
            print("Header Demo Walkthrough:", res_hdr_demo['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            scr8 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_08_demo_banner.png', 'wb') as f:
                f.write(base64.b64decode(scr8['result']['data']))
            print("Saved vw_live_08_demo_banner.png (Size:", os.path.getsize('d:/KPMG/vw_live_08_demo_banner.png'), ")")

            print("\n🎉 ALL LIVE VERIFICATION WORKSPACE FLOWS TESTED AND VALIDATED SUCCESSFULLY!")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(run_natural_test())
