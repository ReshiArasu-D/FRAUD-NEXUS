import asyncio, subprocess, requests, json, websockets, base64, sys, os

sys.stdout.reconfigure(encoding='utf-8')

async def run_vw_walkthrough():
    print("=== LIVE VERIFICATION WORKSPACE WALKTHROUGH ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_vw_live'
    port = 9310
    
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
            await asyncio.sleep(6)

            async def click_element_by_text(tag, text_contains):
                js = f"""
                (() => {{
                    const els = Array.from(document.querySelectorAll("{tag}"));
                    const el = els.find(e => (e.innerText || '').includes("{text_contains}"));
                    if (!el) return null;
                    const r = el.getBoundingClientRect();
                    return JSON.stringify({{ x: r.left + r.width / 2, y: r.top + r.height / 2, width: r.width, height: r.height }});
                }})()
                """
                res = await send('Runtime.evaluate', {'expression': js, 'returnByValue': True})
                val = res['result']['result'].get('value')
                if not val:
                    return False
                coords = json.loads(val)
                if coords['width'] == 0 or coords['height'] == 0:
                    return False
                await send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
                await send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
                return True

            async def click_element_by_selector(sel):
                js = f"""
                (() => {{
                    const el = document.querySelector("{sel}");
                    if (!el) return null;
                    const r = el.getBoundingClientRect();
                    return JSON.stringify({{ x: r.left + r.width / 2, y: r.top + r.height / 2 }});
                }})()
                """
                res = await send('Runtime.evaluate', {'expression': js, 'returnByValue': True})
                val = res['result']['result'].get('value')
                if not val:
                    return False
                coords = json.loads(val)
                await send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
                await send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
                return True

            # Step 1: Click 'Get Started'
            print("2. Clicking 'Get Started'...")
            c1 = await click_element_by_text('button', 'Get Started')
            print("Clicked Get Started:", c1)
            await asyncio.sleep(2)

            # Step 2: Click 'Enter Investigator Workspace'
            print("3. Clicking 'Enter Investigator Workspace'...")
            c2 = await click_element_by_text('button', 'Investigator')
            print("Clicked Enter Investigator Workspace:", c2)
            await asyncio.sleep(2)

            # Step 3: Click 'Demo Quick Login'
            print("4. Clicking 'Demo Quick Login'...")
            c3 = await click_element_by_text('button', 'Demo Quick Login')
            print("Clicked Demo Quick Login:", c3)
            await asyncio.sleep(3)

            # Step 4: Click 'Investigation' in Sidebar
            print("5. Clicking 'Investigation' in Admin Sidebar...")
            c4 = await click_element_by_text('.fnx-sidebar-item, button', 'Investigation')
            print("Clicked Investigation Sidebar:", c4)
            await asyncio.sleep(2)

            # 6. Capture Verification Workspace Overview Screenshot
            print("6. Capturing Screenshot: VW Overview...")
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_01_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Saved vw_real_01_overview.png")

            # 7. Click Evidence Nav
            print("7. Clicking Evidence Left Nav...")
            c_ev = await click_element_by_text('.fnx-lnav-btn', 'Evidence')
            print("Clicked Evidence:", c_ev)
            await asyncio.sleep(1.5)

            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_02_evidence.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Saved vw_real_02_evidence.png")

            # 8. Click Cyber Analysis Nav
            print("8. Clicking Cyber Analysis Left Nav...")
            c_cy = await click_element_by_text('.fnx-lnav-btn', 'Cyber Analysis')
            print("Clicked Cyber Analysis:", c_cy)
            await asyncio.sleep(1.5)

            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_03_cyber.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Saved vw_real_03_cyber.png")

            # 9. Click Partner Requests Nav
            print("9. Clicking Partner Requests Left Nav...")
            c_pr = await click_element_by_text('.fnx-lnav-btn', 'Partner Requests')
            print("Clicked Partner Requests:", c_pr)
            await asyncio.sleep(1.5)

            scr4 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_04_partner.png', 'wb') as f:
                f.write(base64.b64decode(scr4['result']['data']))
            print("Saved vw_real_04_partner.png")

            # 10. Click 'Generative Intelligence' Header Action
            print("10. Clicking Header Action: Generative Intelligence...")
            c_gen = await click_element_by_text('.fnx-btn-header', 'Generative Intelligence')
            print("Clicked GenAI Header Action:", c_gen)
            await asyncio.sleep(2)

            scr5 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_05_genai_modal.png', 'wb') as f:
                f.write(base64.b64decode(scr5['result']['data']))
            print("Saved vw_real_05_genai_modal.png")

            # Close GenAI modal
            await click_element_by_selector('.btn-close-modal')
            await asyncio.sleep(1)

            # 11. Click Human Decision Nav
            print("11. Clicking Human Decision Left Nav...")
            c_dec = await click_element_by_text('.fnx-lnav-btn', 'Human Decision')
            print("Clicked Human Decision:", c_dec)
            await asyncio.sleep(1.5)

            scr6 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_06_decision.png', 'wb') as f:
                f.write(base64.b64decode(scr6['result']['data']))
            print("Saved vw_real_06_decision.png")

            # 12. Click Case Reports Nav
            print("12. Clicking Case Reports Left Nav...")
            c_rep = await click_element_by_text('.fnx-lnav-btn', 'Case Reports')
            print("Clicked Case Reports:", c_rep)
            await asyncio.sleep(1.5)

            scr7 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_07_report.png', 'wb') as f:
                f.write(base64.b64decode(scr7['result']['data']))
            print("Saved vw_real_07_report.png")

            # 13. Click 'Demo Walkthrough' Header Button
            print("13. Clicking Header Action: Demo Walkthrough...")
            c_walk = await click_element_by_text('.fnx-btn-header', 'Demo Walkthrough')
            print("Clicked Demo Walkthrough:", c_walk)
            await asyncio.sleep(1.5)

            scr8 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_real_08_demo_banner.png', 'wb') as f:
                f.write(base64.b64decode(scr8['result']['data']))
            print("Saved vw_real_08_demo_banner.png")

            print("\n🎉 ALL REAL INTERACTION STEPS COMPLETED!")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(run_vw_walkthrough())
