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
            const nav = document.querySelectorAll('.fnx-nav-item')[3];
            const hpNav = document.querySelectorAll('.fnx-nav-item')[4];
            const cs = window.getComputedStyle(nav);
            const csHp = window.getComputedStyle(hpNav);
            const csHpView = document.querySelector('.fnx-help-view') ? window.getComputedStyle(document.querySelector('.fnx-help-view')) : null;
            return {
                nav_transition: cs.transition,
                nav_animation: cs.animation,
                hpNav_transition: csHp.transition,
                hpNav_animation: csHp.animation,
                hpView_transition: csHpView ? csHpView.transition : null,
                hpView_animation: csHpView ? csHpView.animation : null
            };
        })())
        """
        res = await eval_js(test_script)
        val = res.get('result', {}).get('result', {}).get('value')
        print(val)

asyncio.run(main())
