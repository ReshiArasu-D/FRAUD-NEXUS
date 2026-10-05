import asyncio, json, requests, websockets, sys, base64
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    resp = requests.get('http://127.0.0.1:9222/json')
    targets = resp.json()
    target = next(t for t in targets if 'fnx' in t.get('url', ''))
    ws_url = target['webSocketDebuggerUrl']
    async with websockets.connect(ws_url, max_size=25000000) as ws:
        msg_id = 1
        
        async def call_cdp(method, params=None):
            nonlocal msg_id
            cur_id = msg_id
            msg_id += 1
            cmd = {'id': cur_id, 'method': method, 'params': params or {}}
            await ws.send(json.dumps(cmd))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == cur_id:
                    return msg

        async def eval_js(expr):
            res = await call_cdp('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            return res.get('result', {}).get('result', {}).get('value')

        print("1. Checking current view...", flush=True)
        v = await eval_js("(() => (angular.element(document.querySelector('.fnx-app')).scope() || {}).c.currentView)()")
        print(f"Current view is: {v}", flush=True)

        if v == 'landing' or not v:
            print("Logging into customer portal via loadDemoSession...", flush=True)
            await eval_js("""
            (() => {
                const el = document.querySelector('.fnx-app') || document.querySelector('[ng-controller]');
                const scope = angular.element(el).scope();
                const c = scope.c;
                c.loadDemoSession();
                scope.$apply();
            })()
            """)
            await asyncio.sleep(1)

        print("\n2. Clicking Evidence in sidebar...", flush=True)
        ev_state = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            navItems[3].click();
            const c = angular.element(document.querySelector('.fnx-app')).scope().c;
            return {
                view: c.currentView,
                activePills: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                isEvidenceVaultInDom: !!document.querySelector('.fnx-evidence-vault'),
                isHelpInDom: !!document.querySelector('.fnx-help-view'),
                evidenceVaultTitle: document.querySelector('.fnx-evidence-vault .fnx-page-title') ? document.querySelector('.fnx-evidence-vault .fnx-page-title').innerText : null
            };
        })()
        """)
        print("Evidence View State:", json.dumps(ev_state, indent=2), flush=True)

        # Capture Screenshot of Evidence Vault
        print("Capturing evidence_vault_verified.png...", flush=True)
        shot1 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/evidence_vault_verified.png', 'wb') as f:
            f.write(base64.b64decode(shot1['result']['data']))
        print("Saved d:/KPMG/evidence_vault_verified.png", flush=True)

        print("\n3. Clicking Help & Support in sidebar...", flush=True)
        help_state = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            navItems[4].click();
            const c = angular.element(document.querySelector('.fnx-app')).scope().c;
            return {
                view: c.currentView,
                activePills: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                isEvidenceVaultInDom: !!document.querySelector('.fnx-evidence-vault'),
                isHelpInDom: !!document.querySelector('.fnx-help-view'),
                helpTitle: document.querySelector('.fnx-help-view .fnx-page-title') ? document.querySelector('.fnx-help-view .fnx-page-title').innerText : null,
                has1930EmergencyHelpline: !!document.querySelector('.fnx-help-view a[href="tel:1930"]')
            };
        })()
        """)
        print("Help View State:", json.dumps(help_state, indent=2), flush=True)

        # Capture Screenshot of Help & Support
        print("Capturing help_support_verified.png...", flush=True)
        shot2 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/help_support_verified.png', 'wb') as f:
            f.write(base64.b64decode(shot2['result']['data']))
        print("Saved d:/KPMG/help_support_verified.png", flush=True)

        print("\n4. Clicking back to Evidence to verify bidirectional navigation...", flush=True)
        ev_state_return = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            navItems[3].click();
            const c = angular.element(document.querySelector('.fnx-app')).scope().c;
            return {
                view: c.currentView,
                activePills: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                isEvidenceVaultInDom: !!document.querySelector('.fnx-evidence-vault'),
                isHelpInDom: !!document.querySelector('.fnx-help-view')
            };
        })()
        """)
        print("Return to Evidence State:", json.dumps(ev_state_return, indent=2), flush=True)

asyncio.run(main())
