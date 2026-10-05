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

        # Check console logs and errors or exceptions
        test_script = """
        JSON.stringify((() => {
            const ev = document.querySelector('.fnx-evidence-vault');
            const hp = document.querySelector('.fnx-help-view');
            return {
                ev_data_ng_animate: ev ? ev.getAttribute('data-ng-animate') : null,
                hp_data_ng_animate: hp ? hp.getAttribute('data-ng-animate') : null,
                ev_classes: ev ? ev.className : null,
                hp_classes: hp ? hp.className : null,
                navItems_animate: Array.from(document.querySelectorAll('.fnx-nav-item')).map(a => ({
                    text: a.innerText.replace(/\\s+/g, ' ').trim(),
                    anim: a.getAttribute('data-ng-animate'),
                    classes: a.className
                }))
            };
        })())
        """
        res = await eval_js(test_script)
        val = res.get('result', {}).get('result', {}).get('value')
        print(val)

asyncio.run(main())
