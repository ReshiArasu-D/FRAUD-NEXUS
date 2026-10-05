import asyncio, json, requests, websockets, sys, base64
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    resp = requests.get('http://127.0.0.1:9222/json')
    targets = resp.json()
    target = next(t for t in targets if 'fnx' in t.get('url', ''))
    ws_url = target['webSocketDebuggerUrl']
    async with websockets.connect(ws_url, max_size=25000000) as ws:
        msg_id = 1
        async def eval_js(expr):
            nonlocal msg_id
            cmd = {'id': msg_id, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}
            msg_id += 1
            await ws.send(json.dumps(cmd))
            while True:
                m = json.loads(await ws.recv())
                if m.get('id') == cmd['id']:
                    res_val = m.get('result', {}).get('result', {})
                    return res_val.get('value', res_val)

        async def send(method, params=None):
            nonlocal msg_id
            cmd = {'id': msg_id, 'method': method, 'params': params or {}}
            msg_id += 1
            await ws.send(json.dumps(cmd))
            while True:
                m = json.loads(await ws.recv())
                if m.get('id') == cmd['id']:
                    return m

        # 1. Log into customer portal
        print("Logging into customer portal via loadDemoSession...")
        login_res = await eval_js("""
        (() => {
            const el = document.querySelector('.fnx-app') || document.querySelector('[ng-controller]');
            const scope = angular.element(el).scope();
            const c = scope.c;
            c.loadDemoSession();
            scope.$apply();
            return {
                view: c.currentView,
                user: c.user ? c.user.name : null,
                navCount: document.querySelectorAll('.fnx-nav-item').length
            };
        })()
        """)
        print("Login result:", json.dumps(login_res, indent=2))
        await asyncio.sleep(1)

        # 2. Test clicking Evidence Vault
        print("\n--- 2. NAVIGATING TO EVIDENCE VAULT ---")
        ev_test = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            // Click Evidence (index 3)
            navItems[3].click();
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                currentView: c.currentView,
                activeNavs: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evidenceVaultRendered: !!document.querySelector('.fnx-evidence-vault'),
                evidenceVaultTitle: document.querySelector('.fnx-evidence-vault .fnx-page-title') ? document.querySelector('.fnx-evidence-vault .fnx-page-title').innerText : null,
                helpViewRendered: !!document.querySelector('.fnx-help-view')
            };
        })()
        """)
        print("Evidence View State:", json.dumps(ev_test, indent=2))
        await asyncio.sleep(1)

        # Screenshot of Evidence Vault
        s1 = await send('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/evidence_vault_verified.png', 'wb') as f:
            f.write(base64.b64decode(s1['result']['data']))
        print("--> Captured: d:/KPMG/evidence_vault_verified.png")

        # 3. Test clicking Help & Support
        print("\n--- 3. NAVIGATING TO HELP & SUPPORT ---")
        help_test = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            // Click Help & Support (index 4)
            navItems[4].click();
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                currentView: c.currentView,
                activeNavs: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evidenceVaultRendered: !!document.querySelector('.fnx-evidence-vault'),
                helpViewRendered: !!document.querySelector('.fnx-help-view'),
                helpTitle: document.querySelector('.fnx-help-view .fnx-page-title') ? document.querySelector('.fnx-help-view .fnx-page-title').innerText : null,
                emergencyHelpline1930Present: !!document.querySelector('.fnx-help-view a[href="tel:1930"]')
            };
        })()
        """)
        print("Help & Support View State:", json.dumps(help_test, indent=2))
        await asyncio.sleep(1)

        # Screenshot of Help & Support
        s2 = await send('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/help_support_verified.png', 'wb') as f:
            f.write(base64.b64decode(s2['result']['data']))
        print("--> Captured: d:/KPMG/help_support_verified.png")

        # 4. Click back to Evidence to verify seamless back-and-forth
        print("\n--- 4. NAVIGATING BACK TO EVIDENCE ---")
        ev_test2 = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            navItems[3].click();
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                currentView: c.currentView,
                activeNavs: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evidenceVaultRendered: !!document.querySelector('.fnx-evidence-vault'),
                helpViewRendered: !!document.querySelector('.fnx-help-view')
            };
        })()
        """)
        print("Evidence View State (Return):", json.dumps(ev_test2, indent=2))

asyncio.run(main())
