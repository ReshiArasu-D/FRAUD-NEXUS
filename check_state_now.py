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

        res = await eval_js("""
        (() => {
            const app = document.querySelector('.fnx-app');
            if (!app) return { app: false, body: document.body.innerText.substring(0, 300) };
            const scope = angular.element(app).scope();
            const c = scope ? scope.c : null;
            return {
                app: true,
                hasC: !!c,
                user: c ? c.user : null,
                currentView: c ? c.currentView : null,
                navCount: document.querySelectorAll('.fnx-nav-item').length
            };
        })()
        """)
        print(res.get('result', {}).get('result', {}).get('value'))

asyncio.run(main())
