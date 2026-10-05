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

        print("1. Navigating to Track Cases...", flush=True)
        res_track = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            scope.c.navigate('trackCases');
            scope.$apply();
            return {
                view: scope.c.currentView,
                caseCount: (scope.c.cases || []).length,
                hasSelectedCase: !!scope.c.selectedCase,
                aiButtonsCount: document.querySelectorAll('.fnx-btn-ai').length
            };
        })()
        """)
        print("Track Cases State:", json.dumps(res_track, indent=2), flush=True)
        await asyncio.sleep(0.5)

        print("\n2. Clicking Generative Summary on first case card in list...", flush=True)
        res_summary = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const firstCase = scope.c.cases[0];
            scope.c.toggleCaseSummary(firstCase);
            scope.$apply();
            return {
                caseNumber: firstCase.number,
                showAiSummary: firstCase.showAiSummary,
                hasAiSummaryObject: !!firstCase.aiSummary,
                headline: firstCase.aiSummary ? firstCase.aiSummary.headline : null,
                narrative: firstCase.aiSummary ? firstCase.aiSummary.narrative : null,
                summaryCardRendered: !!document.querySelector('.fnx-case-card .fnx-ai-summary-card')
            };
        })()
        """)
        print("Generative Summary Expanded:", json.dumps(res_summary, indent=2), flush=True)
        await asyncio.sleep(1)

        # Capture screenshot of Track Cases with Generative Summary expanded
        print("Capturing track_cases_generative_summary.png...", flush=True)
        shot1 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/track_cases_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(shot1['result']['data']))
        print("Saved d:/KPMG/track_cases_generative_summary.png", flush=True)

        print("\n3. Clicking View Details to enter Case Detail Workspace...", flush=True)
        res_detail = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const firstCase = scope.c.cases[0];
            scope.c.viewCase(firstCase);
            scope.$apply();
            return {
                hasSelectedCase: !!scope.c.selectedCase,
                selectedCaseNumber: scope.c.selectedCase ? scope.c.selectedCase.number : null,
                detailWorkspaceRendered: !!document.querySelector('.fnx-case-detail-workspace'),
                detailAiSummaryCardRendered: !!document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card'),
                trackerStepsCount: document.querySelectorAll('.fnx-detail-tracker .fnx-tracker-step').length
            };
        })()
        """)
        print("Case Detail Workspace State:", json.dumps(res_detail, indent=2), flush=True)
        await asyncio.sleep(1)

        # Capture screenshot of Case Detail Workspace
        print("Capturing case_detail_generative_summary.png...", flush=True)
        shot2 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/case_detail_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(shot2['result']['data']))
        print("Saved d:/KPMG/case_detail_generative_summary.png", flush=True)

asyncio.run(main())
