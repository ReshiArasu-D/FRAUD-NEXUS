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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9255',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile31',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9255/json/new?about:blank')
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
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)

            # Click Login button in landing header
            click_login_script = """
            (() => {
                const btns = Array.from(document.querySelectorAll('.fnx-landing-actions button'));
                const loginBtn = btns.find(b => b.innerText.includes('Login'));
                if (loginBtn) { loginBtn.click(); return "CLICKED_LOGIN"; }
                return "LOGIN_BTN_NOT_FOUND";
            })()
            """
            res1 = await send('Runtime.evaluate', {'expression': click_login_script, 'returnByValue': True})
            print("Step 1 (Click Login):", res1['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Type credentials and click Submit
            # First register a fresh user to guarantee login works
            fill_and_login_script = """
            (() => {
                const emailInput = document.querySelector('input[type="email"]');
                const passInput = document.querySelector('input[type="password"]');
                const submitBtn = document.querySelector('.fnx-auth-form button[type="submit"], .fnx-auth-form button');
                
                if (!emailInput || !passInput || !submitBtn) {
                    return "INPUTS_NOT_FOUND";
                }
                
                emailInput.value = 'arun.fnx.1790945880@example.com';
                emailInput.dispatchEvent(new Event('input', { bubbles: true }));
                emailInput.dispatchEvent(new Event('change', { bubbles: true }));
                
                passInput.value = 'DemoPass123!';
                passInput.dispatchEvent(new Event('input', { bubbles: true }));
                passInput.dispatchEvent(new Event('change', { bubbles: true }));
                
                submitBtn.click();
                return "SUBMITTED_LOGIN";
            })()
            """
            res2 = await send('Runtime.evaluate', {'expression': fill_and_login_script, 'returnByValue': True})
            print("Step 2 (Fill & Submit):", res2['result']['result'].get('value'))
            
            # Wait 5 seconds for login response and dashboard render
            await asyncio.sleep(5)

            # Take screenshot of Dashboard
            shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_logged_in_dashboard.png', 'wb') as f:
                f.write(base64.b64decode(shot['result']['data']))
            print("Captured screenshot_logged_in_dashboard.png")

            # Check DOM for dashboard elements
            check_dom = """
            (() => {
                return JSON.stringify({
                    hasDashboard: !!document.querySelector('.fnx-dashboard'),
                    hasSidebar: !!document.querySelector('.fnx-sidebar'),
                    welcomeText: document.querySelector('.fnx-welcome h2')?.innerText,
                    statsTotal: document.querySelector('.fnx-stat-val')?.innerText,
                    navItems: Array.from(document.querySelectorAll('.fnx-nav-label')).map(n => n.innerText)
                });
            })()
            """
            res3 = await send('Runtime.evaluate', {'expression': check_dom, 'returnByValue': True})
            print("Dashboard DOM check:\n", res3['result']['result'].get('value'))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
