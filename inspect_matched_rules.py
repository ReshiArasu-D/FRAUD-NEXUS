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
            return res.get('result', {}).get('result', {}).get('value')

        res = await eval_js("""
        (() => {
            const evEl = document.querySelectorAll('.fnx-nav-item')[3];
            const helpEl = document.querySelectorAll('.fnx-nav-item')[4];
            
            // Check matched CSS rules
            function getMatchingRules(el) {
                const matched = [];
                for (const sheet of document.styleSheets) {
                    try {
                        for (const rule of sheet.cssRules) {
                            if (rule.selectorText && el.matches(rule.selectorText)) {
                                matched.push({
                                    selector: rule.selectorText,
                                    bg: rule.style.backgroundColor || rule.style.background,
                                    color: rule.style.color
                                });
                            }
                        }
                    } catch(e) {}
                }
                return matched;
            }

            return {
                ev_outerHTML: evEl.outerHTML,
                help_outerHTML: helpEl.outerHTML,
                ev_rules: getMatchingRules(evEl),
                help_rules: getMatchingRules(helpEl)
            };
        })()
        """)
        print(json.dumps(res, indent=2))

asyncio.run(main())
