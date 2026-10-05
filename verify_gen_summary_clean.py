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

        print("1. Reloading page with cache ignore...", flush=True)
        await call_cdp('Page.reload', {'ignoreCache': True})
        await asyncio.sleep(4)

        print("2. Restoring customer demo session...", flush=True)
        await eval_js("""
        (() => {
            const el = document.querySelector('.fnx-app') || document.querySelector('[ng-controller]');
            const scope = angular.element(el).scope();
            const c = scope.c;
            c.loadDemoSession();
            scope.$apply();
        })()
        """)
        await asyncio.sleep(1)

        print("3. Navigating to Track Cases...", flush=True)
        track_info = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            scope.c.navigate('trackCases');
            scope.$apply();
            return {
                view: scope.c.currentView,
                caseCount: (scope.c.cases || []).length,
                aiButtonsCount: document.querySelectorAll('.fnx-btn-ai').length
            };
        })()
        """)
        print("Track Cases Info:", json.dumps(track_info, indent=2), flush=True)

        print("\n4. Clicking Generative Summary on first case card...", flush=True)
        summary_info = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const c = scope.c;
            const cs = c.cases[0];
            c.toggleCaseSummary(cs);
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
        print("Summary Result:", json.dumps(summary_info, indent=2), flush=True)
        await asyncio.sleep(1)

        # Capture Screenshot of Track Cases with Summary expanded
        print("Capturing track_cases_generative_summary.png...", flush=True)
        s1 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/track_cases_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(s1['result']['data']))
        print("Saved d:/KPMG/track_cases_generative_summary.png", flush=True)

        print("\n5. Clicking View Details to open full Case Detail View...", flush=True)
        detail_info = await eval_js("""
        (() => {
            const scope = angular.element(document.querySelector('.fnx-app')).scope();
            const c = scope.c;
            const cs = c.cases[0];
            c.viewCase(cs);
            scope.$apply();
            return {
                selectedCase: c.selectedCase.number,
                workspacePresent: !!document.querySelector('.fnx-case-detail-workspace'),
                aiCardPresent: !!document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card'),
                narrativePresent: !!(document.querySelector('.fnx-case-detail-workspace .fnx-ai-summary-card p') || {}).innerText
            };
        })()
        """)
        print("Case Detail Info:", json.dumps(detail_info, indent=2), flush=True)
        await asyncio.sleep(1)

        # Capture Screenshot of Case Detail View with Generative Summary
        print("Capturing case_detail_generative_summary.png...", flush=True)
        s2 = await call_cdp('Page.captureScreenshot', {'format': 'png'})
        with open('d:/KPMG/case_detail_generative_summary.png', 'wb') as f:
            f.write(base64.b64decode(s2['result']['data']))
        print("Saved d:/KPMG/case_detail_generative_summary.png", flush=True)

asyncio.run(main())
