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
        (() => {
            const root = document.querySelector('.fnx-app');
            const c = angular.element(root).scope().c;
            return {
                view: c.currentView,
                active: Array.from(document.querySelectorAll('.fnx-nav-item.active')).map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                evVaultPresent: !!document.querySelector('.fnx-evidence-vault'),
                helpPresent: !!document.querySelector('.fnx-help-view')
            };
        })()
        """
        res = await eval_js(test_script)
        print("res:", json.dumps(res, indent=2))

asyncio.run(main())
