import asyncio, subprocess, requests, json, websockets, sys, time
sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9297',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile66',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9297/json/new?about:blank')
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
            await asyncio.sleep(6)

            # 1. Click Get Started
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click()'})
            await asyncio.sleep(1)

            # 2. Click Enter Customer Portal
            await send('Runtime.evaluate', {'expression': 'Array.from(document.querySelectorAll(".fnx-portal-card button")).find(b => b.innerText.includes("Enter Customer Portal")).click()'})
            await asyncio.sleep(1)

            # 3. Click Register tab
            await send('Runtime.evaluate', {'expression': 'Array.from(document.querySelectorAll(".fnx-auth-tabs button")).find(b => b.innerText.includes("Register")).click()'})
            await asyncio.sleep(1)

            test_email = f"deepika.{int(time.time())}@example.com"
            fill_res = await send('Runtime.evaluate', {'expression': f"""
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
                
                var form = document.querySelector("form.fnx-auth-form");
                var submitBtn = form ? form.querySelector("button[type='submit']") : null;
                if (submitBtn) {{
                    submitBtn.click();
                    return "SUBMIT CLICKED";
                }}
                return "SUBMIT NOT FOUND";
            }})();
            """})
            print("FILL AND SUBMIT RESULT:", fill_res['result']['result'].get('value'))
            await asyncio.sleep(3)

            # Check state after submit
            state = await send('Runtime.evaluate', {'expression': """
            JSON.stringify({
                authError: document.querySelector(".fnx-auth-error") ? document.querySelector(".fnx-auth-error").innerText : null,
                regSuccess: !!document.querySelector(".fnx-reg-success-box"),
                cid: document.querySelector(".fnx-cid-badge") ? document.querySelector(".fnx-cid-badge").innerText : null,
                bodyText: document.querySelector(".fnx-auth-box") ? document.querySelector(".fnx-auth-box").innerText.substring(0, 200) : "no auth box"
            })
            """})
            print("STATE AFTER REGISTRATION:", state['result']['result'].get('value'))
    finally:
        proc.terminate()

asyncio.run(test())
