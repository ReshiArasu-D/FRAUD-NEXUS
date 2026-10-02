import asyncio
import subprocess
import requests
import json
import websockets
import base64
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    port = 9288
    profile_dir = r'd:\KPMG\.edge_temp_profile88'
    
    print(f"Launching Edge on port {port}...")
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--remote-debugging-port={port}',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1400,1050',
        f'--user-data-dir={profile_dir}',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        await asyncio.sleep(2)
        r_new = requests.put(f'http://localhost:{port}/json/new?about:blank')
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

            async def screenshot(filename):
                snap = await send('Page.captureScreenshot', {'format': 'png'})
                img_data = snap.get('result', {}).get('data', '')
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(img_data))
                print(f"Saved: {filename}")

            await send('Page.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx?id=fnx_home'})

            # Wait for Angular / page load
            for _ in range(25):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-app")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            # Inject authenticated customer session and setup Report Fraud View
            setup_script = """
            (function() {
                var el = document.querySelector('.fnx-app');
                if (!el) return false;
                var scope = angular.element(el).scope();
                if (!scope || !scope.c) return false;

                scope.c.user = {
                    sys_id: 'usr_test_arun_123',
                    name: 'Arun Kumar',
                    email: 'arun.kumar@example.com'
                };
                scope.c.customer = {
                    sys_id: 'cust_test_arun_123',
                    customer_id: 'CNX-2026-001034',
                    name: 'Arun Kumar',
                    mobile: '9876543210',
                    email: 'arun.kumar@example.com',
                    kyc_status: 'Verified'
                };
                scope.c.currentView = 'reportFraud';
                scope.c.reportStep = 1;
                scope.c.caseSubmittedSuccess = false;
                
                // Prefill clean realistic data
                scope.c.reportForm.type = 'Payment Fraud';
                scope.c.reportForm.title = 'UPI payment made but product not received';
                scope.c.reportForm.description = 'Victim transferred ₹5,000 via PhonePe UPI to a vendor on an online electronics store. Payment was confirmed debited but vendor blocked contact and deleted listing.';
                scope.c.reportForm.incident_date = '2026-10-01';
                scope.c.reportForm.incident_time = '14:30';
                scope.c.reportForm.specific_category = 'Online Shopping Fraud / Fake QR Code';
                scope.c.reportForm.severity = 'High';
                scope.c.reportForm.platform = 'UPI';
                scope.c.reportForm.reference_number = 'UPI-REF-9876543210';
                scope.c.reportForm.money_lost = 'Yes';
                scope.c.reportForm.financial_involvement = 'Yes';
                scope.c.reportForm.exposure = 5000;
                scope.c.reportForm.currency = 'INR (₹)';
                scope.c.reportForm.num_transactions = 1;
                
                // Location data
                scope.c.reportForm.location = 'Chennai';
                scope.c.reportForm.city = 'Chennai';
                scope.c.reportForm.area = 'T. Nagar';
                scope.c.reportForm.specific_location = 'Near Panagal Park Metro';
                scope.c.reportForm.pincode = '600017';
                scope.c.reportForm.state = 'Tamil Nadu';
                scope.c.reportForm.country = 'India';
                scope.c.reportForm.digital_platform = 'UPI (PhonePe)';
                
                // Financial data
                scope.c.reportForm.institution_type = 'Bank / Financial Institution';
                scope.c.reportForm.institution_name = 'State Bank of India';
                scope.c.reportForm.branch = 'T. Nagar Branch';
                scope.c.reportForm.payment_mode = 'UPI';
                scope.c.reportForm.reference_type = 'UTR';
                scope.c.reportForm.transaction_reference = 'UPI-REF-9876543210';
                
                // People data
                scope.c.reportForm.suspect_name = 'Fraudulent Merchant Electronics';
                scope.c.reportForm.suspect_contact = '+91 98765 43210';
                scope.c.reportForm.suspect_email = 'support@fraud-electronics.in';
                scope.c.reportForm.suspect_identifier = 'merchant.pay@okhdfcbank';
                scope.c.reportForm.suspect_url = 'https://fake-gadget-mart.xyz';
                scope.c.reportForm.communication_channel = 'WhatsApp';
                
                // Evidence data
                scope.c.reportForm.evidence_type = 'Screenshot';
                scope.c.reportForm.evidence_description = 'Payment debit screenshot from PhonePe app showing UTR';
                
                scope.$apply();
                return true;
            })();
            """
            
            res = await send('Runtime.evaluate', {'expression': setup_script})
            print(f"Setup evaluation: {res.get('result', {}).get('result', {}).get('value')}")
            await asyncio.sleep(1)

            # Step 1: Incident Details
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 1; s.c.caseSubmittedSuccess = false; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_01_incident_details.png')

            # Step 2: Location
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 2; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_02_location.png')

            # Step 3: Financial Information
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 3; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_03_financial_info.png')

            # Step 4: People / Entities
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 4; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_04_people_entities.png')

            # Step 5: Evidence
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 5; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_05_evidence.png')

            # Step 6: Review & Confirm
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 6; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_06_review.png')

            # Step 7: Submit Declaration
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 7; s.c.caseSubmittedSuccess = false; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_07_submit_declaration.png')

            # Step 7: Case Submitted Success State
            await send('Runtime.evaluate', {'expression': 'var s = angular.element(document.querySelector(".fnx-app")).scope(); s.c.reportStep = 7; s.c.caseSubmittedSuccess = true; s.c.submittedCaseNumber = "FNX-2026-001034"; s.$apply();'})
            await asyncio.sleep(0.5)
            await screenshot('rf_08_case_submitted_success.png')

            print("All 7 steps + submission success screen captured successfully!")

    finally:
        proc.kill()

if __name__ == '__main__':
    asyncio.run(main())
