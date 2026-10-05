import asyncio, json, requests, websockets, sys, base64
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
            return Array.from(document.querySelectorAll('.fnx-nav-item')).map(a => ({
                text: a.innerText.replace(/\\s+/g, ' ').trim(),
                className: a.className,
                bg: window.getComputedStyle(a).backgroundColor,
                color: window.getComputedStyle(a).color
            }));
        })()
        """)
        print(json.dumps(res, indent=2))

        # Capture Screenshot
        shot = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/help_support_verified_now.png', 'wb') as f:
            f.write(base64.b64decode(shot['result']['data']))
        print("Saved d:/KPMG/help_support_verified_now.png")

asyncio.run(main())
