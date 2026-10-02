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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9254',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile30',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9254/json/new?about:blank')
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
            await send('Runtime.enable')
            await send('Console.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)

            # Switch view to dashboard and catch any exceptions
            setup_script = """
            (() => {
                try {
                    const scope = angular.element(document.querySelector(".fnx-app")).scope();
                    scope.c.user = { sys_id: "123", name: "Arun Kumar", email: "arun.kumar@example.com" };
                    scope.c.customer = { customer_id: "CNX-2026-001001", status: "Verified" };
                    scope.c.stats = { total: 3, active: 2, resolved: 1, closed: 0 };
                    scope.c.cases = [
                        { number: "FNX-2026-001001", type: "Payment Fraud", date: "2026-10-01", severity: "High", status: "Investigation", exposure: "45000" }
                    ];
                    scope.c.currentView = 'dashboard';
                    scope.$apply();
                    return "APPLIED_SUCCESS";
                } catch(e) {
                    return "APPLY_ERROR: " + e.message + " stack: " + e.stack;
                }
            })()
            """
            res = await send('Runtime.evaluate', {'expression': setup_script, 'returnByValue': True})
            print("Apply result:\n", res['result']['result'].get('value'))

            await asyncio.sleep(1)
            # Check if any exception was logged
            eval_dom = await send('Runtime.evaluate', {
                'expression': 'JSON.stringify({hasDashboard: !!document.querySelector(".fnx-dashboard"), text: document.body.innerText.substring(0, 500)})',
                'returnByValue': True
            })
            print("DOM check:\n", eval_dom['result']['result'].get('value'))

            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/dashboard_live.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Captured dashboard_live.png")
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
