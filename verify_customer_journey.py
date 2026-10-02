import asyncio
import subprocess
import requests
import json
import websockets
import base64
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9280',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile80',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9280/json/new?about:blank')
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

            # Wait for landing hero
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-hero-btns button")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break
            
            # Reset language to English at start
            await send('Runtime.evaluate', {'expression': """
            (function() {
                localStorage.setItem('fnx_lang', 'en');
                var sel = document.querySelector(".fnx-lang-select");
                if (sel && sel.value !== 'en') {
                    sel.value = 'en';
                    sel.dispatchEvent(new Event('change', {bubbles: true}));
                }
            })();
            """})
            await asyncio.sleep(0.5)

            # --- 1. LANDING PAGE ---
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_01_landing.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 1: Captured Landing Page (ux_01_landing.png)", flush=True)

            # Check 13 languages in select
            opts = await send('Runtime.evaluate', {'expression': 'document.querySelectorAll(".fnx-lang-select option").length'})
            print("Language options count:", opts.get('result', {}).get('result', {}).get('value'), flush=True)

            # --- 2. PORTAL SELECTION ---
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-hero-btns button").click()'})
            await asyncio.sleep(1.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_02_portal_select.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 2: Captured Portal Selection (ux_02_portal_select.png)", flush=True)

            # --- 3. CUSTOMER PORTAL AUTH (LOGIN) ---
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-portal-card.fnx-portal-customer button").click()'
            })
            await asyncio.sleep(1.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_03_login.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 3: Captured Login View (ux_03_login.png)", flush=True)

            # --- 4. REGISTRATION FORM ---
            await send('Runtime.evaluate', {
                'expression': 'document.querySelectorAll(".fnx-auth-tabs button")[1].click()'
            })
            await asyncio.sleep(1.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_04_register_form.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 4: Captured Registration Form (ux_04_register_form.png)", flush=True)

            # --- 5. FILL REGISTRATION & SUBMIT ---
            test_email = f"deepika.{int(time.time())}@example.com"
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
            
            # Wait for reg success
            for _ in range(15):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-reg-success-box")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_05_register_success.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 5: Captured Registration Success (ux_05_register_success.png)", flush=True)

            # --- 6. CLICK GO TO LOGIN & PERFORM LOGIN ---
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-reg-success-box button").click()'
            })
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
            
            # Wait for dashboard
            for _ in range(20):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-dashboard")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_06_dashboard.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 6: Captured Customer Dashboard (ux_06_dashboard.png)", flush=True)

            # --- 7. CUSTOMER PROFILE & KYC ---
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-profile-pill").click()'})
            await asyncio.sleep(1.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_07_profile_kyc.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 7: Captured Profile & KYC View (ux_07_profile_kyc.png)", flush=True)

            # Submit KYC
            kyc_code = """
            (function() {
                var inp = document.querySelector("input[ng-model='c.kycForm.idNumber']");
                if (inp) {
                    inp.value = "987654321012";
                    inp.dispatchEvent(new Event('input', {bubbles: true}));
                    inp.dispatchEvent(new Event('change', {bubbles: true}));
                }
                var btn = document.querySelector(".fnx-kyc-card button.fnx-btn-primary");
                if (btn) btn.click();
            })();
            """
            await send('Runtime.evaluate', {'expression': kyc_code})
            await asyncio.sleep(2.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_08_kyc_submitted.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 8: Captured KYC Submitted View (ux_08_kyc_submitted.png)", flush=True)

            # --- 8. REPORT FRAUD WIZARD ---
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-nav-item[ng-click*=\'reportFraud\']").click()'
            })
            await asyncio.sleep(1.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_09_report_fraud.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 9: Captured Report Fraud Wizard (ux_09_report_fraud.png)", flush=True)

            # Submit Case
            case_code = """
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
                var btn = document.querySelector("form.fnx-wizard-form button.fnx-btn-primary");
                if (btn) btn.click();
            })();
            """
            await send('Runtime.evaluate', {'expression': case_code})
            
            # Wait for case submission success
            for _ in range(15):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-submit-success-card")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_10_case_submitted.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 10: Captured Case Submitted Success (ux_10_case_submitted.png)", flush=True)

            # --- 9. TRACK CASES VIEW ---
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-submit-success-card button.fnx-btn-primary").click()'
            })
            await asyncio.sleep(2)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_11_track_cases.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 11: Captured Track Cases with 5-stage tracker (ux_11_track_cases.png)", flush=True)

            # --- 10. AI ASSISTANT ---
            await send('Runtime.evaluate', {'expression': 'document.querySelector(".fnx-ai-trigger").click()'})
            await asyncio.sleep(1)
            ai_chat_code = """
            (function() {
                var inp = document.querySelector(".fnx-ai-footer input");
                if (inp) {
                    inp.value = "What is the status of my UPI fraud report?";
                    inp.dispatchEvent(new Event('input', {bubbles: true}));
                }
                var btn = Array.from(document.querySelectorAll(".fnx-ai-footer button")).find(b => b.innerText.includes("Send"));
                if (btn) btn.click();
            })();
            """
            await send('Runtime.evaluate', {'expression': ai_chat_code})
            await asyncio.sleep(1.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_12_ai_assistant.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 12: Captured Floating AI Assistant (ux_12_ai_assistant.png)", flush=True)

            # --- 11. LANGUAGE SWITCHING TO TAMIL ---
            await send('Runtime.evaluate', {
                'expression': '''
                (function() {
                    var sel = document.querySelector(".fnx-header-right .fnx-lang-select");
                    if (sel) {
                        sel.value = "ta";
                        sel.dispatchEvent(new Event('change', {bubbles: true}));
                    }
                })();
                '''
            })
            await asyncio.sleep(1.5)
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/ux_13_tamil_ui.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Step 13: Captured Tamil Full-Page Translation (ux_13_tamil_ui.png)", flush=True)

    finally:
        proc.terminate()

asyncio.run(test())
