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

        print("1. Checking current view...", flush=True)
        v = await eval_js("(() => (angular.element(document.querySelector('.fnx-app')).scope() || {}).c.currentView)()")
        print(f"Current view is: {v}", flush=True)

        if v != 'trackCases':
            print("Navigating to trackCases...", flush=True)
            await eval_js("""
            (() => {
                const scope = angular.element(document.querySelector('.fnx-app')).scope();
                scope.c.navigate('trackCases');
                scope.$apply();
            })()
            """)
            await asyncio.sleep(0.5)

        print("\n2. Toggling Generative Summary on Case 1...", flush=True)
        res_summary = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const cs = scope.c.cases[0];
            scope.c.toggleCaseSummary(cs);
            scope.$apply();
            return {
                caseNumber: cs.number,
                showAiSummary: cs.showAiSummary,
                aiSummaryText: cs.aiSummary ? cs.aiSummary.narrative : null,
                actionTaken: cs.aiSummary ? cs.aiSummary.actionTaken : null,
                advice: cs.aiSummary ? cs.aiSummary.citizenAdvice : null
            };
        })()
        """)
        print("Generative Summary Result:", json.dumps(res_summary, indent=2), flush=True)
        await asyncio.sleep(0.8)

        print("Capturing track_cases_generative_summary.png...", flush=True)
        s1 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/track_cases_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(s1['result']['data']))
        print("Saved d:/KPMG/track_cases_generative_summary.png", flush=True)

        print("\n3. Opening Case Detail Workspace with viewCase...", flush=True)
        res_detail = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const cs = scope.c.cases[0];
            scope.c.viewCase(cs);
            scope.$apply();
            return {
                selectedCase: scope.c.selectedCase.number,
                workspacePresent: !!document.querySelector('.fnx-case-detail-workspace'),
                detailAiCardPresent: !!document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card'),
                narrativePresent: !!(document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card p') || {}).innerText
            };
        })()
        """)
        print("Case Detail Workspace State:", json.dumps(res_detail, indent=2), flush=True)
        await asyncio.sleep(0.8)

        print("Capturing case_detail_generative_summary.png...", flush=True)
        s2 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/case_detail_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(s2['result']['data']))
        print("Saved d:/KPMG/case_detail_generative_summary.png", flush=True)

asyncio.run(main())
