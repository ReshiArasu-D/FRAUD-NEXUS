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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9263',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile39',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9263/json/new?about:blank')
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

            # Step 1: Click 'Get Started' button using dispatchEvent
            step1_js = """
            (() => {
                const btn = document.querySelector('.fnx-hero-btns button');
                if (btn) {
                    btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                    return "CLICKED_GET_STARTED";
                }
                return "BTN_NOT_FOUND";
            })()
            """
            s1 = await send('Runtime.evaluate', {'expression': step1_js, 'returnByValue': True})
            print("Step 1:", s1['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 2: Click 'Enter Customer Portal'
            step2_js = """
            (() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Enter Customer Portal'));
                if (btn) {
                    btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                    return "CLICKED_ENTER_PORTAL";
                }
                return "PORTAL_BTN_NOT_FOUND";
            })()
            """
            s2 = await send('Runtime.evaluate', {'expression': step2_js, 'returnByValue': True})
            print("Step 2:", s2['result']['result'].get('value'))
            await asyncio.sleep(2)

            # Step 3: Click 'Register' tab
            step3_js = """
            (() => {
                const regTab = Array.from(document.querySelectorAll('.fnx-auth-tabs button')).find(b => b.innerText.includes('Register'));
                if (regTab) {
                    regTab.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                    return "CLICKED_REGISTER_TAB";
                }
                return "REG_TAB_NOT_FOUND";
            })()
            """
            s3 = await send('Runtime.evaluate', {'expression': step3_js, 'returnByValue': True})
            print("Step 3:", s3['result']['result'].get('value'))
            await asyncio.sleep(1)

            # Take screenshot of Register form with eye icons
            shot_reg = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_register_with_eyes.png', 'wb') as f:
                f.write(base64.b64decode(shot_reg['result']['data']))
            print("Saved screenshot_register_with_eyes.png")

            # Check eye icon elements
            check_js = """
            (() => {
                const eyes = Array.from(document.querySelectorAll('.fnx-eye-btn'));
                const inputs = Array.from(document.querySelectorAll('.fnx-password-wrap input'));
                return JSON.stringify({
                    eyeCount: eyes.length,
                    inputs: inputs.map(i => ({ placeholder: i.placeholder, type: i.type }))
                });
            })()
            """
            chk = await send('Runtime.evaluate', {'expression': check_js, 'returnByValue': True})
            print("DOM Check:\n", chk['result']['result'].get('value'))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
