import asyncio, subprocess, requests, json, websockets, base64, sys, os

sys.stdout.reconfigure(encoding='utf-8')

async def run_customer_e2e():
    print("=== STARTING COMPLETE CUSTOMER PORTAL E2E VERIFICATION ===")
    profile_dir = r'd:\KPMG\.edge_temp_profile_cust_flow'
    port = 9298
    
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

            async def eval_js(expr):
                res = await send('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
                return res.get('result', {}).get('result', {}).get('value')

            async def take_screenshot(filename):
                shot = await send('Page.captureScreenshot', {'format': 'png'})
                img_data = base64.b64decode(shot['result']['data'])
                filepath = os.path.join(r'd:\KPMG', filename)
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"  --> Saved screenshot: {filename}")

            await send('Page.enable')
            await send('Runtime.enable')
            
            print("1. Navigating to https://dev187180.service-now.com/fnx...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(5)

            # Step 1: Click 'Get Started'
            print("2. Clicking 'Get Started' on Landing...")
            s1 = await eval_js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(btn => btn.innerText.includes('Get Started'));
                if (b) { b.click(); return 'CLICKED_GET_STARTED'; }
                return 'NOT_FOUND';
            })()
            """)
            print("  Result:", s1)
            await asyncio.sleep(2)

            # Step 2: Click 'Enter Portal' on Customer Card
            print("3. Clicking 'Enter Portal' for Customer Portal...")
            s2 = await eval_js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(btn => btn.innerText.includes('Enter Portal'));
                if (b) { b.click(); return 'CLICKED_ENTER_PORTAL'; }
                return 'NOT_FOUND';
            })()
            """)
            print("  Result:", s2)
            await asyncio.sleep(2)

            # Step 3: Click 'Try Demo'
            print("4. Clicking 'Try Demo' (Judge Access) on Auth Page...")
            s3 = await eval_js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const b = btns.find(btn => btn.innerText.includes('Try Demo') || btn.className.includes('fnx-btn-demo'));
                if (b) { b.click(); return 'CLICKED_TRY_DEMO'; }
                return 'NOT_FOUND';
            })()
            """)
            print("  Result:", s3)
            await asyncio.sleep(3)

            # Step 4: Verify Customer Dashboard
            print("\n5. Checking Customer Dashboard...")
            dash_state = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const title = document.querySelector('.fnx-user-badge, h1');
                const stats = Array.from(document.querySelectorAll('.fnx-stat-card, .fnx-kpi-card')).map(el => el.innerText.replace(/\\n/g, ' '));
                const cases = Array.from(document.querySelectorAll('.fnx-case-item, table tbody tr')).map(el => el.innerText.replace(/\\n/g, ' '));
                return {
                    mainExists: !!main,
                    mainHeight: main ? main.offsetHeight : 0,
                    title: title ? title.innerText : null,
                    stats: stats,
                    casesFound: cases.length,
                    firstCase: cases[0] || null
                };
            })()
            """)
            print("Dashboard State:", json.dumps(dash_state, indent=2))
            await take_screenshot("1_customer_dashboard_live.png")

            # Step 5: Test Chat Assistant Trigger & Interaction
            print("\n6. Testing Floating Chat Assistant on Dashboard...")
            ai_trigger = await eval_js("""
            (() => {
                const trig = document.querySelector('.fnx-ai-trigger');
                return {
                    exists: !!trig,
                    visible: trig ? (trig.offsetWidth > 0 && trig.offsetHeight > 0) : false,
                    text: trig ? trig.innerText : null
                };
            })()
            """)
            print("Chat Assistant Button:", ai_trigger)

            # Open chat drawer
            print("Opening Chat Assistant Drawer...")
            await eval_js("""
            (() => {
                const trig = document.querySelector('.fnx-ai-trigger');
                if (trig) trig.click();
            })()
            """)
            await asyncio.sleep(2)
            await take_screenshot("2_customer_chat_assistant_open.png")

            # Close drawer
            await eval_js("""
            (() => {
                const closeBtn = document.querySelector('.fnx-ai-close');
                if (closeBtn) closeBtn.click();
            })()
            """)
            await asyncio.sleep(1)

            # Step 6: Navigate to Track Cases
            print("\n7. Navigating to 'Track Cases'...")
            t_res = await eval_js("""
            (() => {
                const navLinks = Array.from(document.querySelectorAll('.fnx-nav-item, a, button'));
                const trackLink = navLinks.find(el => el.innerText.includes('Track Cases'));
                if (trackLink) { trackLink.click(); return 'CLICKED_TRACK_CASES'; }
                return 'NOT_FOUND';
            })()
            """)
            print("  Result:", t_res)
            await asyncio.sleep(2)

            track_state = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const track = document.querySelector('.fnx-track-cases, .fnx-track-workspace, [ng-if*=\"trackCases\"]');
                const title = document.querySelector('.fnx-page-title, h1');
                const cards = Array.from(document.querySelectorAll('.fnx-case-card, .fnx-track-card, tr')).map(el => el.innerText.replace(/\\n/g, ' '));
                return {
                    mainHeight: main ? main.offsetHeight : 0,
                    trackExists: !!track,
                    trackInsideMain: main && track ? main.contains(track) : false,
                    trackHeight: track ? track.offsetHeight : 0,
                    trackTop: track ? track.getBoundingClientRect().top : null,
                    pageTitle: title ? title.innerText : null,
                    casesCount: cards.length
                };
            })()
            """)
            print("Track Cases State:", json.dumps(track_state, indent=2))
            await take_screenshot("3_customer_track_cases_live.png")

            # Step 7: Navigate to Evidence
            print("\n8. Navigating to 'Evidence'...")
            e_res = await eval_js("""
            (() => {
                const navLinks = Array.from(document.querySelectorAll('.fnx-nav-item, a, button'));
                const evLink = navLinks.find(el => el.innerText.includes('Evidence'));
                if (evLink) { evLink.click(); return 'CLICKED_EVIDENCE'; }
                return 'NOT_FOUND';
            })()
            """)
            print("  Result:", e_res)
            await asyncio.sleep(2)

            ev_state = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const vault = document.querySelector('.fnx-vault-workspace, .fnx-evidence-view, [ng-if*=\"evidenceVault\"]');
                const title = document.querySelector('.fnx-page-title, h1');
                return {
                    mainHeight: main ? main.offsetHeight : 0,
                    vaultExists: !!vault,
                    vaultInsideMain: main && vault ? main.contains(vault) : false,
                    vaultHeight: vault ? vault.offsetHeight : 0,
                    vaultTop: vault ? vault.getBoundingClientRect().top : null,
                    pageTitle: title ? title.innerText : null
                };
            })()
            """)
            print("Evidence Vault State:", json.dumps(ev_state, indent=2))
            await take_screenshot("4_customer_evidence_live.png")

            # Step 8: Navigate to Help & Support
            print("\n9. Navigating to 'Help & Support'...")
            h_res = await eval_js("""
            (() => {
                const navLinks = Array.from(document.querySelectorAll('.fnx-nav-item, a, button'));
                const hLink = navLinks.find(el => el.innerText.includes('Help & Support') || el.innerText.includes('Help'));
                if (hLink) { hLink.click(); return 'CLICKED_HELP'; }
                return 'NOT_FOUND';
            })()
            """)
            print("  Result:", h_res)
            await asyncio.sleep(2)

            help_state = await eval_js("""
            (() => {
                const main = document.querySelector('main.fnx-content');
                const help = document.querySelector('.fnx-help-workspace, [ng-if*=\"help\"]');
                const title = document.querySelector('.fnx-page-title, h1');
                return {
                    mainHeight: main ? main.offsetHeight : 0,
                    helpExists: !!help,
                    helpInsideMain: main && help ? main.contains(help) : false,
                    helpHeight: help ? help.offsetHeight : 0,
                    helpTop: help ? help.getBoundingClientRect().top : null,
                    pageTitle: title ? title.innerText : null
                };
            })()
            """)
            print("Help & Support State:", json.dumps(help_state, indent=2))
            await take_screenshot("5_customer_help_live.png")

            print("\n=== COMPLETE VERIFICATION FINISHED SUCCESSFULLY ===")

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(run_customer_e2e())
