import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def find_matching_rules():
    profile_dir = r'd:\KPMG\.edge_temp_profile_match_rules'
    port = 9285
    
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--remote-debugging-port={port}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1680,1050',
        f'--user-data-dir={profile_dir}',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        await asyncio.sleep(2)
        r_new = requests.put(f'http://localhost:{port}/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        
        async with websockets.connect(ws_url, max_size=30000000) as ws:
            msg_id = 1
            async def send(method, params=None):
                nonlocal msg_id
                cmd = {'id': msg_id, 'method': method, 'params': params or {}}
                msg_id += 1
                await ws.send(json.dumps(cmd))
                while True:
                    m = json.loads(await ws.recv())
                    if m.get('id') == cmd['id']:
                        return m

            await send('Page.enable')
            await send('Runtime.enable')

            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # Switch to auth view
            switch_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.currentView = 'auth';
                scope.c.authMode = 'login';
                scope.$apply();
                return "AUTH_VIEW_ACTIVE";
            })()
            """
            await send('Runtime.evaluate', {'expression': switch_js, 'returnByValue': True})
            await asyncio.sleep(2)

            # Find matching rules in document.styleSheets
            rules_js = """
            (() => {
                const el = document.querySelector('.fnx-auth-tabs');
                if (!el) return { error: "No .fnx-auth-tabs found" };

                const matched = [];
                for (let sheet of document.styleSheets) {
                    try {
                        const rules = sheet.cssRules || sheet.rules;
                        if (!rules) continue;
                        for (let rule of rules) {
                            if (rule.selectorText && el.matches(rule.selectorText)) {
                                matched.push({
                                    selector: rule.selectorText,
                                    cssText: rule.cssText
                                });
                            }
                        }
                    } catch(e) {}
                }
                return {
                    matched: matched,
                    inlineStyle: el.getAttribute('style')
                };
            })()
            """
            r_rules = await send('Runtime.evaluate', {'expression': rules_js, 'returnByValue': True})
            print("Matched Rules for .fnx-auth-tabs:", json.dumps(r_rules['result']['result'].get('value'), indent=2))

            # Also check .fnx-auth-box and .fnx-auth-right
            box_js = """
            (() => {
                const check = (selector) => {
                    const el = document.querySelector(selector);
                    if (!el) return [];
                    const matched = [];
                    for (let sheet of document.styleSheets) {
                        try {
                            const rules = sheet.cssRules || sheet.rules;
                            if (!rules) continue;
                            for (let rule of rules) {
                                if (rule.selectorText && el.matches(rule.selectorText)) {
                                    matched.push({
                                        selector: rule.selectorText,
                                        cssText: rule.cssText
                                    });
                                }
                            }
                        } catch(e) {}
                    }
                    return matched;
                };
                return {
                    box: check('.fnx-auth-box'),
                    right: check('.fnx-auth-right')
                };
            })()
            """
            r_box = await send('Runtime.evaluate', {'expression': box_js, 'returnByValue': True})
            print("Matched Rules for box & right:", json.dumps(r_box['result']['result'].get('value'), indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(find_matching_rules())
