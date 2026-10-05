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
                    return res if (res := m.get('result', {}).get('result', {}).get('value')) is not None else m

        script = """
        (() => {
            const items = Array.from(document.querySelectorAll('.fnx-nav-item')).map(a => a.outerHTML);
            const contentChildren = Array.from(document.querySelector('.fnx-content').children).map(c => ({
                tagName: c.tagName,
                className: c.className,
                id: c.id,
                display: window.getComputedStyle(c).display,
                ngIf: c.getAttribute('ng-if')
            }));
            return { items, contentChildren };
        })()
        """
        res = await eval_js(script)
        print(json.dumps(res, indent=2))

asyncio.run(main())
