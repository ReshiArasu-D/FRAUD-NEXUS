import asyncio, subprocess, requests, json, websockets, sys, time
sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9298',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile69',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9298/json/new?about:blank')
        ws_url = r_new.json().get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
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
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx?id=fnx_home'})
            
            # Wait for landing page to load
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-hero-btns button")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            # 1. Click Get Started
            r1 = await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click(); "OK"'})
            print("1. Click Get Started:", r1['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            # 2. Click Enter Customer Portal
            r2 = await send('Runtime.evaluate', {'expression': """
            (function() {
                var b = Array.from(document.querySelectorAll(".fnx-portal-card button")).find(b => b.innerText.includes("Enter Customer Portal"));
                if (b) { b.click(); return "CLICKED PORTAL"; }
                return "PORTAL BTN NOT FOUND";
            })()
            """})
            print("2. Click Enter Customer Portal:", r2['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            # 3. Click Register Tab
            r4 = await send('Runtime.evaluate', {'expression': """
            (function() {
                var b = Array.from(document.querySelectorAll(".fnx-auth-tabs button")).find(b => b.innerText.includes("Register"));
                if (b) { b.click(); return "CLICKED REGISTER TAB"; }
                return "REGISTER TAB NOT FOUND";
            })()
            """})
            print("3. Click Register Tab:", r4['result']['result'].get('value'))
            await asyncio.sleep(1.5)

            # 4. Fill Form
            test_email = f"deepika.{int(time.time())}@example.com"
            r6 = await send('Runtime.evaluate', {'expression': f"""
            (function() {{
                function setVal(sel, val) {{
                    var el = document.querySelector(sel);
                    if (el) {{
                        el.value = val;
                        el.dispatchEvent(new Event('input', {{bubbles: true}}));
                        el.dispatchEvent(new Event('change', {{bubbles: true}}));
                    }}
                }}
                setVal("input[ng-model='c.authForm.name']", "Deepika Ramanathan");
                setVal("input[ng-model='c.authForm.mobile']", "9876543210");
                setVal("input[ng-model='c.authForm.email']", "{test_email}");
                setVal("input[ng-model='c.authForm.dob']", "1994-06-15");
                setVal("select[ng-model='c.authForm.gender']", "Female");
                setVal("select[ng-model='c.authForm.occupation']", "Professional");
                setVal("textarea[ng-model='c.authForm.address']", "Flat 4B, Emerald Heights, T. Nagar, Chennai 600017");
                setVal("input[ng-model='c.authForm.password']", "DemoPass123!");
                setVal("input[ng-model='c.authForm.confirmPassword']", "DemoPass123!");
                return "FORM FILLED: {test_email}";
            }})()
            """})
            print("4. Fill Form Result:", r6['result']['result'].get('value'))
            await asyncio.sleep(1)

            # 5. Submit Register Form
            r7 = await send('Runtime.evaluate', {'expression': """
            (function() {
                var btn = document.querySelector(".fnx-auth-box button.fnx-btn-primary");
                if (btn) { btn.click(); return "SUBMIT CLICKED: " + btn.innerText; }
                return "SUBMIT BTN NOT FOUND";
            })()
            """})
            print("5. Submit Form Result:", r7['result']['result'].get('value'))
            await asyncio.sleep(4)

            # 6. Check Post-Submit State
            r8 = await send('Runtime.evaluate', {'expression': """
            JSON.stringify({
                hasSuccess: !!document.querySelector(".fnx-reg-success-box"),
                cid: document.querySelector(".fnx-cid-badge") ? document.querySelector(".fnx-cid-badge").innerText : null,
                authError: document.querySelector(".fnx-auth-error") ? document.querySelector(".fnx-auth-error").innerText : null,
                goToLoginBtn: !!Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Go to Login"))
            })
            """})
            print("6. Post-Submit State:", r8['result']['result'].get('value'))

    finally:
        proc.terminate()

asyncio.run(test())
