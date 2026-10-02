import asyncio, subprocess, requests, json, websockets, sys, time
sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9277',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile75',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9277/json/new?about:blank')
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

            # Wait for landing
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-hero-btns button")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            # Click Get Started -> Portal Select -> Enter Customer Portal
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click()'})
            await asyncio.sleep(1.5)
            await send('Runtime.evaluate', {'expression': 'Array.from(document.querySelectorAll(".fnx-portal-card button")).find(b => b.innerText.includes("Enter Customer Portal")).click()'})
            await asyncio.sleep(1.5)

            # Register
            await send('Runtime.evaluate', {'expression': 'Array.from(document.querySelectorAll(".fnx-auth-tabs button")).find(b => b.innerText.includes("Register")).click()'})
            await asyncio.sleep(1.5)

            test_email = f"cx.test.{int(time.time())}@example.com"
            fill_code = f"""
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
                document.querySelector(".fnx-auth-box button.fnx-btn-primary").click();
            }})();
            """
            await send('Runtime.evaluate', {'expression': fill_code})
            await asyncio.sleep(3)

            # Login
            await send('Runtime.evaluate', {'expression': 'Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Go to Login")).click()'})
            await asyncio.sleep(1.5)
            login_code = f"""
            (function() {{
                function setVal(sel, val) {{
                    var el = document.querySelector(sel);
                    if (el) {{
                        el.value = val;
                        el.dispatchEvent(new Event('input', {{bubbles: true}}));
                        el.dispatchEvent(new Event('change', {{bubbles: true}}));
                    }}
                }}
                setVal("input[ng-model='c.authForm.email']", "{test_email}");
                setVal("input[ng-model='c.authForm.password']", "DemoPass123!");
                document.querySelector(".fnx-auth-box button.fnx-btn-primary").click();
            }})();
            """
            await send('Runtime.evaluate', {'expression': login_code})
            await asyncio.sleep(3)

            # Navigate to Report Fraud
            await send('Runtime.evaluate', {'expression': 'Array.from(document.querySelectorAll(".fnx-nav-item")).find(a => a.innerText.includes("Report Fraud")).click()'})
            await asyncio.sleep(1.5)

            # Inspect Report Fraud form fields and check validity
            inspect_form = await send('Runtime.evaluate', {'expression': """
            JSON.stringify(Array.from(document.querySelectorAll("form.fnx-wizard-form input, form.fnx-wizard-form textarea, form.fnx-wizard-form select")).map(i => ({
                tag: i.tagName,
                model: i.getAttribute("ng-model"),
                type: i.type,
                val: i.value,
                required: i.required,
                valid: i.checkValidity()
            })))
            """})
            print("REPORT FRAUD FORM INITIAL STATE:\n", inspect_form['result']['result'].get('value'))

            # Fill Report Fraud
            fill_case = """
            (function() {
                function setVal(sel, val) {
                    var el = document.querySelector(sel);
                    if (el) {
                        el.value = val;
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
                    }
                }
                setVal("textarea[ng-model='c.reportForm.description']", "Victim received a malicious APK pretending to be electricity bill update; unauthorized UPI debit occurred.");
                setVal("input[ng-model='c.reportForm.incident_date']", "2026-10-01");
                setVal("input[ng-model='c.reportForm.incident_time']", "14:30");
                setVal("input[ng-model='c.reportForm.location']", "Chennai");
                setVal("input[ng-model='c.reportForm.area']", "T. Nagar");
                setVal("input[ng-model='c.reportForm.pincode']", "600017");
                setVal("input[ng-model='c.reportForm.digital_platform']", "Google Pay & WhatsApp");
                setVal("input[ng-model='c.reportForm.institution_name']", "State Bank of India");
                setVal("input[ng-model='c.reportForm.transaction_reference']", "UPI-REF-9988776655");
                setVal("input[ng-model='c.reportForm.exposure']", "35000");
                setVal("input[ng-model='c.reportForm.suspect_name']", "Fraud Beneficiary");
                setVal("input[ng-model='c.reportForm.suspect_contact']", "scammer@upi");
                setVal("input[ng-model='c.reportForm.evidence_description']", "Screenshot of unauthorized UPI debit confirmation SMS");
                return "FILLED CASE";
            })();
            """
            await send('Runtime.evaluate', {'expression': fill_case})
            await asyncio.sleep(1)

            # Check validity again
            valid_chk = await send('Runtime.evaluate', {'expression': """
            JSON.stringify(Array.from(document.querySelectorAll("form.fnx-wizard-form input, form.fnx-wizard-form textarea, form.fnx-wizard-form select")).filter(i => !i.checkValidity()).map(i => ({
                model: i.getAttribute("ng-model"),
                validationMsg: i.validationMessage
            })))
            """})
            print("INVALID FIELDS BEFORE SUBMIT:\n", valid_chk['result']['result'].get('value'))

            # Click submit
            sub_res = await send('Runtime.evaluate', {'expression': """
            (function() {
                var btn = document.querySelector("form.fnx-wizard-form button.fnx-btn-primary");
                if (btn) {
                    btn.click();
                    return "SUBMIT CLICKED: " + btn.innerText;
                }
                return "SUBMIT NOT FOUND";
            })()
            """})
            print("SUBMIT BUTTON CLICK:", sub_res['result']['result'].get('value'))
            await asyncio.sleep(3)

            # Post-submit view
            post_view = await send('Runtime.evaluate', {'expression': """
            JSON.stringify({
                hasSuccessCard: !!document.querySelector(".fnx-submit-success-card"),
                caseNum: document.querySelector(".fnx-submit-success-card strong") ? document.querySelector(".fnx-submit-success-card strong").innerText : null,
                bodyText: document.querySelector(".fnx-content") ? document.querySelector(".fnx-content").innerText.substring(0, 200) : "no content"
            })
            """})
            print("POST SUBMIT CHECK:\n", post_view['result']['result'].get('value'))
    finally:
        proc.terminate()

asyncio.run(test())
