import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def debug_customer():
    profile_dir = r'd:\KPMG\.edge_temp_profile_cust_debug'
    port = 9288
    
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

            print("1. Loading portal...")
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {
                    'expression': 'document.querySelector(".fnx-app") !== null',
                    'returnByValue': True
                })
                if chk['result']['result'].get('value'):
                    break

            # Perform Demo Citizen Login
            print("2. Performing Customer Demo Login...")
            login_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                if (typeof c.doDemoLogin === 'function') {
                    c.doDemoLogin();
                } else {
                    c.user = { name: 'Demo Citizen', email: 'demo@fraudnexus.gov' };
                    c.customer = { customer_id: 'FNX-DEMO-2026', phone: '+91 98765 43210' };
                    c.currentView = 'dashboard';
                }
                scope.$apply();
                return {
                    user: c.user,
                    customer: c.customer,
                    currentView: c.currentView
                };
            })()
            """
            r_login = await send('Runtime.evaluate', {'expression': login_js, 'returnByValue': True})
            print("Login result:", json.dumps(r_login['result']['result'].get('value'), indent=2))
            await asyncio.sleep(2)

            # Check Dashboard view DOM
            print("\n3. Inspecting Dashboard view DOM...")
            dash_check = """
            (() => {
                const content = document.querySelector('.fnx-content');
                return {
                    hasContent: content !== null,
                    htmlLen: content ? content.innerHTML.length : 0,
                    children: content ? Array.from(content.children).map(ch => ({
                        tag: ch.tagName,
                        className: ch.className,
                        offsetParent: ch.offsetParent !== null,
                        clientHeight: ch.clientHeight
                    })) : []
                };
            })()
            """
            r_dash = await send('Runtime.evaluate', {'expression': dash_check, 'returnByValue': True})
            print("Dashboard DOM:", json.dumps(r_dash['result']['result'].get('value'), indent=2))

            # Click or navigate to trackCases
            print("\n4. Navigating to trackCases...")
            track_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.navigate('trackCases');
                scope.$apply();
                
                const content = document.querySelector('.fnx-content');
                const track = document.querySelector('.fnx-track-cases');
                return {
                    currentView: scope.c.currentView,
                    hasTrackElem: track !== null,
                    trackHtml: track ? track.outerHTML.substring(0, 600) : 'NOT_FOUND',
                    trackComputedStyle: track ? {
                        display: window.getComputedStyle(track).display,
                        visibility: window.getComputedStyle(track).visibility,
                        height: window.getComputedStyle(track).height,
                        color: window.getComputedStyle(track).color
                    } : null,
                    contentChildren: content ? Array.from(content.children).map(ch => ({
                        className: ch.className,
                        tag: ch.tagName,
                        visible: ch.offsetParent !== null
                    })) : []
                };
            })()
            """
            r_track = await send('Runtime.evaluate', {'expression': track_js, 'returnByValue': True})
            print("Track Cases inspection:", json.dumps(r_track['result']['result'].get('value'), indent=2))

            # Click or navigate to evidenceVault
            print("\n5. Navigating to evidenceVault...")
            ev_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.navigate('evidenceVault');
                scope.$apply();
                
                const ev = document.querySelector('.fnx-evidence-vault');
                return {
                    currentView: scope.c.currentView,
                    hasEvElem: ev !== null,
                    evHtml: ev ? ev.outerHTML.substring(0, 600) : 'NOT_FOUND',
                    evComputedStyle: ev ? {
                        display: window.getComputedStyle(ev).display,
                        visibility: window.getComputedStyle(ev).visibility,
                        height: window.getComputedStyle(ev).height
                    } : null
                };
            })()
            """
            r_ev = await send('Runtime.evaluate', {'expression': ev_js, 'returnByValue': True})
            print("Evidence Vault inspection:", json.dumps(r_ev['result']['result'].get('value'), indent=2))

            # Click or navigate to help
            print("\n6. Navigating to help...")
            help_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                scope.c.navigate('help');
                scope.$apply();
                
                const help = document.querySelector('.fnx-help-view');
                return {
                    currentView: scope.c.currentView,
                    hasHelpElem: help !== null,
                    helpHtml: help ? help.outerHTML.substring(0, 600) : 'NOT_FOUND',
                    helpComputedStyle: help ? {
                        display: window.getComputedStyle(help).display,
                        visibility: window.getComputedStyle(help).visibility,
                        height: window.getComputedStyle(help).height
                    } : null
                };
            })()
            """
            r_help = await send('Runtime.evaluate', {'expression': help_js, 'returnByValue': True})
            print("Help inspection:", json.dumps(r_help['result']['result'].get('value'), indent=2))

            # Inspect AI Trigger / Floating Chat button
            print("\n7. Inspecting Chat Assistant in Customer View...")
            ai_js = """
            (() => {
                const el = document.querySelector('.fnx-app');
                const scope = angular.element(el).scope();
                const c = scope.c;
                
                const allAi = Array.from(document.querySelectorAll('*')).filter(el => {
                    const cl = (el.className || '').toString();
                    return cl.includes('ai-') || cl.includes('chat') || (el.innerText && el.innerText.includes('Ask FRAUDNEXUS'));
                });
                
                return {
                    showAI: c.showAI,
                    aiDrawerInDOM: document.querySelector('.fnx-ai-drawer') !== null || document.querySelector('.fnx-admin-ai-drawer') !== null,
                    aiElements: allAi.map(e => ({
                        tag: e.tagName,
                        className: e.className,
                        visible: e.offsetParent !== null,
                        rect: e.getBoundingClientRect()
                    }))
                };
            })()
            """
            r_ai = await send('Runtime.evaluate', {'expression': ai_js, 'returnByValue': True})
            print("AI Assistant inspection:", json.dumps(r_ai['result']['result'].get('value'), indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(debug_customer())
