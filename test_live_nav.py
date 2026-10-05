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
                    res_val = m.get('result', {}).get('result', {})
                    return res_val.get('value', res_val)

        test_script = """
        (() => {
            const root = document.querySelector('.fnx-app');
            const scope = angular.element(root).scope();
            const c = scope.c;
            
            c.navigate('help');
            scope.$apply();
            
            const afterHelp = {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
            
            c.navigate('evidenceVault');
            scope.$apply();
            
            const afterEv = {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
            
            return { afterHelp, afterEv };
        })()
        """
        res = await eval_js(test_script)
        print("Navigation test result:")
        print(json.dumps(res, indent=2))

asyncio.run(main())
