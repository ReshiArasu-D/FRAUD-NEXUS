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

        print("1. Navigating to trackCases...")
        res1 = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            scope.c.navigate('trackCases');
            scope.$apply();
            return {
                view: scope.c.currentView,
                caseCount: scope.c.cases.length,
                aiButtons: document.querySelectorAll('.fnx-btn-ai').length
            };
        })()
        """)
        print("Track Cases State:", json.dumps(res1, indent=2))
        await asyncio.sleep(0.5)

        print("\n2. Toggling Generative Summary on Case 1...")
        res2 = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const cs = scope.c.cases[0];
            scope.c.toggleCaseSummary(cs);
            scope.$apply();
            return {
                caseNumber: cs.number,
                showAiSummary: cs.showAiSummary,
                aiSummary: cs.aiSummary,
                cardRendered: !!document.querySelector('.fnx-case-card .fnx-ai-summary-card')
            };
        })()
        """)
        print("Generative Summary Card State:", json.dumps(res2, indent=2))
        await asyncio.sleep(1)

        # Capture Screenshot of Track Cases with Generative Summary expanded
        print("Capturing track_cases_generative_summary.png...")
        shot1 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/track_cases_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(shot1['result']['data']))
        print("Saved d:/KPMG/track_cases_generative_summary.png")

        print("\n3. Opening Case Detail Workspace with viewCase...")
        res3 = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const cs = scope.c.cases[0];
            scope.c.viewCase(cs);
            scope.$apply();
            return {
                selectedCase: scope.c.selectedCase.number,
                workspacePresent: !!document.querySelector('.fnx-case-detail-workspace'),
                detailAiCardPresent: !!document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card'),
                headline: document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card p') ? document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card p').innerText : null
            };
        })()
        """)
        print("Case Detail Workspace State:", json.dumps(res3, indent=2))
        await asyncio.sleep(1)

        # Capture Screenshot of Case Detail Workspace with Generative AI Summary
        print("Capturing case_detail_generative_summary.png...")
        shot2 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/case_detail_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(shot2['result']['data']))
        print("Saved d:/KPMG/case_detail_generative_summary.png")

asyncio.run(main())
