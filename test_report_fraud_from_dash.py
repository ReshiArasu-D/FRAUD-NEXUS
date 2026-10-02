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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9257',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile33',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9257/json/new?about:blank')
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

            # Click Login
            await send('Runtime.evaluate', {'expression': "Array.from(document.querySelectorAll('.fnx-landing-actions button')).find(b => b.innerText.includes('Login')).click()"})
            await asyncio.sleep(2)

            # Fill and submit login
            login_js = """
            (() => {
                const e = document.querySelector('input[type="email"]');
                const p = document.querySelector('input[type="password"]');
                e.value = 'arun.fnx.1790945880@example.com';
                e.dispatchEvent(new Event('input', { bubbles: true }));
                p.value = 'DemoPass123!';
                p.dispatchEvent(new Event('input', { bubbles: true }));
                document.querySelector('.fnx-auth-form button').click();
            })()
            """
            await send('Runtime.evaluate', {'expression': login_js})
            await asyncio.sleep(5)

            # Now on dashboard, click 'Report Fraud' button
            click_rf = """
            (() => {
                const btn = document.querySelector('.fnx-action-row button');
                if (btn) { btn.click(); return "CLICKED_ACTION_ROW_BTN"; }
                const nav = Array.from(document.querySelectorAll('.fnx-nav-item')).find(n => n.innerText.includes('Report Fraud'));
                if (nav) { nav.click(); return "CLICKED_NAV_ITEM"; }
                return "BTN_NOT_FOUND";
            })()
            """
            res_rf = await send('Runtime.evaluate', {'expression': click_rf, 'returnByValue': True})
            print("Click Report Fraud:", res_rf['result']['result'].get('value'))
            await asyncio.sleep(2)

            shot_wizard = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_rf_wizard_real.png', 'wb') as f:
                f.write(base64.b64decode(shot_wizard['result']['data']))
            print("Saved screenshot_rf_wizard_real.png")

            # Click AI button
            await send('Runtime.evaluate', {'expression': "document.querySelector('.fnx-ai-fab')?.click()"})
            await asyncio.sleep(1)

            shot_ai = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_ai_open_real.png', 'wb') as f:
                f.write(base64.b64decode(shot_ai['result']['data']))
            print("Saved screenshot_ai_open_real.png")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
