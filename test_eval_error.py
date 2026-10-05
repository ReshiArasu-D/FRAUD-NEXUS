import asyncio, json, requests, websockets, sys
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
            return res.get('result', {})

        print("Testing eval_js...")
        res = await eval_js("""
        (() => {
            try {
                const el = document.querySelector('.fnx-app') || document.querySelector('[ng-controller]');
                if (!el) return { error: 'No app or ng-controller found' };
                const scope = angular.element(el).scope();
                if (!scope || !scope.c) return { error: 'No scope or c found' };
                scope.c.loadDemoSession();
                scope.$apply();
                return {
                    view: scope.c.currentView,
                    user: scope.c.user.name,
                    casesCount: scope.c.cases.length
                };
            } catch(e) {
                return { exception: e.toString() };
            }
        })()
        """)
        print("Login Result:", json.dumps(res, indent=2))

asyncio.run(main())
