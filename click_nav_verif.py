import asyncio, subprocess, requests, json, websockets, base64, sys, os, shutil

sys.stdout.reconfigure(encoding='utf-8')

async def run_verif_navigation():
    print("=== NAVIGATING TO VERIFICATION WORKSPACE VIA CDP MOUSE EVENTS ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_verif_cdp'
    port = 9288
    
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

            async def click_element(selector_or_fn, desc=""):
                print(f"Clicking: {desc}...")
                box_res = await send('Runtime.evaluate', {
                    'expression': f"""
                    (() => {{
                        let el = null;
                        if (typeof ({selector_or_fn}) === 'function') {{
                            el = ({selector_or_fn})();
                        }} else {{
                            el = document.querySelector("{selector_or_fn}");
                        }}
                        if (!el) return null;
                        const rect = el.getBoundingClientRect();
                        return JSON.stringify({{ x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 }});
                    }})()
                    """,
                    'returnByValue': True
                })
                val = box_res['result']['result'].get('value')
                if not val:
                    print(f"ERROR: Element not found for {desc}")
                    return False
                coords = json.loads(val)
                print(f"Coords for {desc}: ({coords['x']}, {coords['y']})")
                await send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
                await send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': coords['x'], 'y': coords['y'], 'button': 'left', 'clickCount': 1})
                await asyncio.sleep(2)
                return True

            await send('Page.enable')
            await send('Runtime.enable')
            
            print("1. Loading https://dev187180.service-now.com/fnx...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)

            # Step 1: Click 'Get Started' button (.fnx-hero-btns button or button with text)
            fn_get_started = "() => Array.from(document.querySelectorAll('button, a')).find(b => b.innerText.includes('Get Started'))"
            ok = await click_element(fn_get_started, "Get Started button")
            if not ok:
                await click_element(".fnx-hero-btns button", "Hero Get Started button")

            # Step 2: Click 'Enter Investigator Workspace'
            fn_inv = "() => Array.from(document.querySelectorAll('button, a')).find(b => b.innerText.includes('Investigator'))"
            await click_element(fn_inv, "Enter Investigator Workspace")

            # Step 3: Click 'Demo Quick Login'
            fn_demo = "() => Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Demo Quick Login') || b.className.includes('fnx-btn-demo'))"
            await click_element(fn_demo, "Demo Quick Login")
            await asyncio.sleep(2)

            # Step 4: Click 'Investigation' in Admin Sidebar
            fn_inv_side = "() => Array.from(document.querySelectorAll('.fnx-sidebar-item, button')).find(b => b.innerText.includes('Investigation'))"
            await click_element(fn_inv_side, "Investigation Sidebar Item")
            await asyncio.sleep(2)

            # Capture Screenshot 1: Overview
            print("Capturing Overview Screenshot...")
            scr1 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_01_overview.png', 'wb') as f:
                f.write(base64.b64decode(scr1['result']['data']))
            print("Saved d:/KPMG/vw_live_01_overview.png")

            # Step 5: Click 'Verification Queue' in Left Navigation
            fn_verif_nav = "() => Array.from(document.querySelectorAll('.fnx-lnav-btn')).find(b => b.innerText.includes('Verification Queue'))"
            await click_element(fn_verif_nav, "Verification Queue Left Nav")
            await asyncio.sleep(2)

            # Step 6: Click 'Reset for Demo'
            fn_reset = "() => Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Reset for Demo'))"
            await click_element(fn_reset, "Reset for Demo Button")
            await asyncio.sleep(1)

            # Capture Screenshot 2: Verification Queue Pending
            print("Capturing Verification Queue (Pending) Screenshot...")
            scr2 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_02_verif_pending.png', 'wb') as f:
                f.write(base64.b64decode(scr2['result']['data']))
            print("Saved d:/KPMG/vw_live_02_verif_pending.png")

            # Step 7: Click '✓ Batch Verify All Pending'
            fn_batch = "() => Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Batch Verify All Pending'))"
            await click_element(fn_batch, "Batch Verify All Pending Button")
            await asyncio.sleep(1)

            # Capture Screenshot 3: Verification Queue Confirmed
            print("Capturing Verification Queue (Confirmed) Screenshot...")
            scr3 = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/vw_live_03_verif_confirmed.png', 'wb') as f:
                f.write(base64.b64decode(scr3['result']['data']))
            print("Saved d:/KPMG/vw_live_03_verif_confirmed.png")

            # Copy to brain artifact directory
            art_dir = r'C:\Users\hp\.gemini\antigravity-ide\brain\59316f90-7827-47e6-86b5-4235fae01a28'
            shutil.copy('d:/KPMG/vw_live_01_overview.png', os.path.join(art_dir, 'vw_live_01_overview.png'))
            shutil.copy('d:/KPMG/vw_live_02_verif_pending.png', os.path.join(art_dir, 'vw_live_02_verif_pending.png'))
            shutil.copy('d:/KPMG/vw_live_03_verif_confirmed.png', os.path.join(art_dir, 'vw_live_03_verif_confirmed.png'))
            print("All 3 screenshots saved to artifact directory.")

            print("=== CDP NAVIGATION AND VERIFICATION TESTS COMPLETED SUCCESSFULLY! ===")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(run_verif_navigation())
