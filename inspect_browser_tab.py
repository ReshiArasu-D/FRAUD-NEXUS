import asyncio, json, requests, websockets, sys
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    try:
        resp = requests.get('http://127.0.0.1:9222/json')
        targets = resp.json()
    except Exception as e:
        print("Cannot connect to port 9222:", e)
        return

    target = None
    for t in targets:
        if 'fnx' in t.get('url', ''):
            target = t
            break

    if not target:
        print("FNX target not found on 9222")
        return

    ws_url = target['webSocketDebuggerUrl']
    async with websockets.connect(ws_url) as ws:
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

        check_script = """
        (() => {
            const el = document.querySelector('.fnx-app') || document.querySelector('[ng-controller]');
            if (!el) return 'No angular element found';
            const scope = angular.element(el).scope();
            const c = scope.c;
            return {
                currentView: c.currentView,
                sidebarItems: Array.from(document.querySelectorAll('.fnx-nav-item')).map(a => ({
                    text: a.innerText.trim(),
                    classes: a.className,
                    clickAttr: a.getAttribute('ng-click'),
                    ngClassAttr: a.getAttribute('ng-class')
                })),
                evidenceVaultVisible: !!document.querySelector('.fnx-evidence-vault'),
                helpViewVisible: !!document.querySelector('.fnx-help-view')
            };
        })()
        """
        info = await eval_js(check_script)
        print("DOM & Angular Info:")
        print(json.dumps(info, indent=2))

asyncio.run(main())
