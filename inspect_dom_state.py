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
            try {
                const root = document.querySelector('.fnx-app');
                const scope = angular.element(root).scope();
                const c = scope.c;
                return {
                    view: c.currentView,
                    allNavs: Array.from(document.querySelectorAll('.fnx-nav-item')).map(a => ({
                        text: a.innerText.replace(/\\s+/g, ' ').trim(),
                        className: a.className,
                        ngClass: a.getAttribute('ng-class')
                    })),
                    evVaultEl: !!document.querySelector('.fnx-evidence-vault'),
                    helpEl: !!document.querySelector('.fnx-help-view'),
                    editProfEl: !!document.querySelector('.fnx-edit-profile-view')
                };
            } catch (e) {
                return { error: e.toString() };
            }
        })())
        """
        res = await eval_js(test_script)
        print("Navigation test result:")
        val = res.get('result', {}).get('result', {}).get('value')
        print(val)

asyncio.run(main())
