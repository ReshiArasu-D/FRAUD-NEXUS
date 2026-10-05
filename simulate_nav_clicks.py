import asyncio, json, requests, websockets, sys
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    resp = requests.get('http://127.0.0.1:9222/json')
    targets = resp.json()
    target = next(t for t in targets if 'fnx' in t.get('url', ''))
    ws_url = target['webSocketDebuggerUrl']
    async with websockets.connect(ws_url) as ws:
        msg_id = 1
        async def eval_js(expr):
            nonlocal msg_id
            cmd = {'id': msg_id, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}
            msg_id += 1
            await ws.send(json.dumps(cmd))
            while True:
                m = json.loads(await ws.recv())
                if m.get('id') == cmd['id']:
                    return m

        test_script = """
        JSON.stringify((() => {
            const navItems = document.querySelectorAll('.fnx-nav-item');
            // Click Help & Support
            navItems[4].click();
            const afterClickHelp = {
                view: angular.element(document.querySelector('.fnx-app')).scope().c.currentView,
                helpClass: navItems[4].className,
                evClass: navItems[3].className,
                evVaultEl: !!document.querySelector('.fnx-evidence-vault'),
                helpEl: !!document.querySelector('.fnx-help-view')
            };
            
            // Now click Evidence
            navItems[3].click();
            const afterClickEv = {
                view: angular.element(document.querySelector('.fnx-app')).scope().c.currentView,
                helpClass: navItems[4].className,
                evClass: navItems[3].className,
                evVaultEl: !!document.querySelector('.fnx-evidence-vault'),
                helpEl: !!document.querySelector('.fnx-help-view')
            };
            
            return { afterClickHelp, afterClickEv };
        })())
        """
        res = await eval_js(test_script)
        val = res.get('result', {}).get('result', {}).get('value')
        print(val)

asyncio.run(main())
