import asyncio
import subprocess
import requests
import json
import websockets
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9253',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile29',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9253/json/new?about:blank')
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
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)

            # Set user state to show dashboard
            setup_script = """
            (() => {
                const scope = angular.element(document.querySelector(".fnx-app")).scope();
                scope.c.user = { name: "Arun Kumar", email: "arun.kumar@example.com" };
                scope.c.customer = { u_customer_id: "CNX-2026-001001", u_status: "Verified" };
                scope.c.stats = { total: 3, active: 2, resolved: 1, closed: 0 };
                scope.c.cases = [
                    { number: "FNX-2026-001001", u_incident_type: "Payment Fraud", u_incident_date: "2026-10-01", u_severity: "High", state: "Investigation", u_financial_exposure: "45000" },
                    { number: "FNX-2026-001002", u_incident_type: "Identity Theft", u_incident_date: "2026-10-02", u_severity: "Medium", state: "Initial Review", u_financial_exposure: "0" }
                ];
                scope.c.currentView = 'dashboard';
                scope.$apply();
            })()
            """
            await send('Runtime.evaluate', {'expression': setup_script})
            await asyncio.sleep(1)

            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_dashboard.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Saved screenshot_dashboard.png")

            # Also check Report Fraud wizard
            await send('Runtime.evaluate', {
                'expression': 'const scope = angular.element(document.querySelector(".fnx-app")).scope(); scope.c.currentView = "reportFraud"; scope.$apply();'
            })
            await asyncio.sleep(1)
            shot_rf = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_report_fraud.png', 'wb') as f:
                f.write(base64.b64decode(shot_rf['result']['data']))
            print("Saved screenshot_report_fraud.png")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
