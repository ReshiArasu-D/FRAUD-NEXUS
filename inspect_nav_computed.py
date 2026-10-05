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
                    return m.get('result', {}).get('result', {}).get('value')

        res = await eval_js("""
        (() => {
            const navItems = Array.from(document.querySelectorAll('.fnx-nav-item')).map(a => ({
                text: a.innerText.replace(/\\s+/g, ' ').trim(),
                className: a.className,
                computedBg: window.getComputedStyle(a).backgroundColor,
                computedColor: window.getComputedStyle(a).color,
                ngClass: a.getAttribute('ng-class')
            }));
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            return {
                currentView: scope.c.currentView,
                navItems
            };
        })()
        """)
        print(json.dumps(res, indent=2))

asyncio.run(main())
