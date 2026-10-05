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
                msg_str = await ws.recv()
                msg = json.loads(msg_str)
                if msg.get('id') == cur_id:
                    return msg

        async def eval_js(expr):
            res = await call_cdp('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            return res.get('result', {}).get('result', {}).get('value')

        # 1. Open Generative Summary on Case 1 in Track Cases list
        print("1. Opening Generative Summary on Case 1 in Track Cases list...", flush=True)
        await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const cs = scope.c.cases[0];
            cs.showAiSummary = true;
            scope.c.generateCaseSummary(cs);
            cs.aiSummaryLoading = false;
            scope.$apply();
        })()
        """)
        await asyncio.sleep(0.5)

        shot1 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/track_cases_with_summary_opened.png', 'wb') as f:
            f.write(base64.b64decode(shot1['result']['data']))
        print("Saved d:/KPMG/track_cases_with_summary_opened.png", flush=True)

        # 2. Click View Details on Case 1 to open Case Detail Workspace
        print("2. Opening Case Detail Workspace...", flush=True)
        await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const cs = scope.c.cases[0];
            scope.c.viewCase(cs);
            cs.aiSummaryLoading = false;
            scope.$apply();
        })()
        """)
        await asyncio.sleep(0.5)

        shot2 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/case_detail_with_summary.png', 'wb') as f:
            f.write(base64.b64decode(shot2['result']['data']))
        print("Saved d:/KPMG/case_detail_with_summary.png", flush=True)

asyncio.run(main())
