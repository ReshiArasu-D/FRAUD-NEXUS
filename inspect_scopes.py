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
            const ev = document.querySelector('.fnx-evidence-vault');
            const hp = document.querySelector('.fnx-help-view');
            const root = document.querySelector('.fnx-app');
            return {
                root_currentView: angular.element(root).scope().c.currentView,
                ev_scope_currentView: ev ? angular.element(ev).scope().c.currentView : null,
                hp_scope_currentView: hp ? angular.element(hp).scope().c.currentView : null,
                ev_parent: ev ? ev.parentElement.className : null,
                hp_parent: hp ? hp.parentElement.className : null,
                html_snippet_around_ev: ev ? ev.outerHTML.substring(0, 300) : null,
                html_snippet_around_hp: hp ? hp.outerHTML.substring(0, 300) : null
            };
        })()
        """
        res = await eval_js(script)
        print(json.dumps(res, indent=2))

asyncio.run(main())
