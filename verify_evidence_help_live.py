import asyncio, json, requests, websockets, sys, time, base64
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

        # Reload the page
        print("Reloading page...")
        await send('Page.reload', {'ignoreCache': True})
        await asyncio.sleep(4)

        # 1. Check initial state
        state1 = await eval_js("""
        (() => {
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
        })()
        """)
        print("Initial state after reload:", json.dumps(state1, indent=2))

        # 2. Click Evidence
        print("\n--- Clicking Evidence ---")
        click_ev = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            navItems[3].click();
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
        })()
        """)
        print("After clicking Evidence:", json.dumps(click_ev, indent=2))
        await asyncio.sleep(1)

        # Take screenshot of Evidence
        s1 = await send('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/evidence_vault_verified.png', 'wb') as f:
            f.write(base64.b64decode(s1['result']['data']))
        print("Saved d:/KPMG/evidence_vault_verified.png")

        # 3. Click Help & Support
        print("\n--- Clicking Help & Support ---")
        click_help = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            navItems[4].click();
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
        })()
        """)
        print("After clicking Help & Support:", json.dumps(click_help, indent=2))
        await asyncio.sleep(1)

        # Take screenshot of Help & Support
        s2 = await send('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/help_support_verified.png', 'wb') as f:
            f.write(base64.b64decode(s2['result']['data']))
        print("Saved d:/KPMG/help_support_verified.png")

        # 4. Click Evidence again to verify back-and-forth toggling
        print("\n--- Clicking Evidence Again ---")
        click_ev2 = await eval_js("""
        (() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            navItems[3].click();
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
        })()
        """)
        print("After clicking Evidence second time:", json.dumps(click_ev2, indent=2))

asyncio.run(main())
