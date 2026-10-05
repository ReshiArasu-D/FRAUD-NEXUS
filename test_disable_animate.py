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
            // Disable $animate
            const root = document.querySelector('.fnx-app');
            const injector = angular.element(root).injector();
            if (injector.has('$animate')) {
                const $animate = injector.get('$animate');
                $animate.enabled(false);
            }
            
            // Add style to kill ng-animate
            const style = document.createElement('style');
            style.innerHTML = `
                .ng-animate {
                    transition: none !important;
                    animation: none !important;
                }
            `;
            document.head.appendChild(style);

            // Clean up any stuck elements and test navigation
            const c = angular.element(root).scope().c;
            
            // Navigate to evidenceVault
            c.navigate('evidenceVault');
            angular.element(root).scope().$apply();
            
            const afterEv = {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
            
            // Navigate to help
            c.navigate('help');
            angular.element(root).scope().$apply();
            
            const afterHelp = {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };

            // Navigate back to evidenceVault
            c.navigate('evidenceVault');
            angular.element(root).scope().$apply();
            
            const afterEv2 = {
                view: c.currentView,
                activeNav: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
            
            return { afterEv, afterHelp, afterEv2 };
        })())
        """
        res = await eval_js(test_script)
        val = res.get('result', {}).get('result', {}).get('value')
        print(val)

asyncio.run(main())
