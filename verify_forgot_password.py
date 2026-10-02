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
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9275',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile48',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9275/json/new?about:blank')
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
            for _ in range(20):
                await asyncio.sleep(1)
                chk = await send('Runtime.evaluate', {'expression': '!!document.querySelector(".fnx-landing-hero")'})
                if chk.get('result', {}).get('result', {}).get('value'):
                    break

            # 1. Click 'Get Started'
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-hero-btns button").click()'
            })
            await asyncio.sleep(1.5)

            # 2. Click 'Enter Customer Portal'
            await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Enter Customer Portal")).click()'
            })
            await asyncio.sleep(1.5)

            # 3. We are on the Login tab: Verify 'Forgot Password?' link is present
            chk_link = await send('Runtime.evaluate', {
                'expression': '!!document.querySelector(".fnx-forgot-pwd")'
            })
            has_forgot_link = chk_link.get('result', {}).get('result', {}).get('value')
            print(f"Has .fnx-forgot-pwd link: {has_forgot_link}")

            # Capture screenshot of login page with Forgot Password
            shot_login = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_login_with_forgot.png', 'wb') as f:
                f.write(base64.b64decode(shot_login['result']['data']))
            print("Saved screenshot_login_with_forgot.png")

            # 4. Click 'Forgot Password?' link
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-forgot-pwd").click()'
            })
            await asyncio.sleep(1)

            # Capture screenshot of Forgot Password form
            shot_forgot = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_forgot_form.png', 'wb') as f:
                f.write(base64.b64decode(shot_forgot['result']['data']))
            print("Saved screenshot_forgot_form.png")

            # 5. Type email and submit reset
            await send('Runtime.evaluate', {
                'expression': '''
                (function() {
                    var inp = document.querySelector("input[ng-model='c.authForm.forgotEmail']");
                    if (inp) {
                        inp.value = "reshirasu@gmail.com";
                        inp.dispatchEvent(new Event('input', {bubbles: true}));
                        inp.dispatchEvent(new Event('change', {bubbles: true}));
                    }
                    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Send Reset Link") || b.innerText.includes("Sending"));
                    if (btn) btn.click();
                })()
                '''
            })
            await asyncio.sleep(2)

            # Capture screenshot of reset confirmation
            shot_confirm = await send('Page.captureScreenshot', {'format': 'png'})
            with open('d:/KPMG/screenshot_forgot_sent.png', 'wb') as f:
                f.write(base64.b64decode(shot_confirm['result']['data']))
            print("Saved screenshot_forgot_sent.png")

            # 6. Click 'Back to Login'
            await send('Runtime.evaluate', {
                'expression': 'document.querySelector(".fnx-back-login").click()'
            })
            await asyncio.sleep(1)

            # Verify back on login
            chk_back = await send('Runtime.evaluate', {
                'expression': '!!document.querySelector("input[ng-model=\'c.authForm.password\']")'
            })
            print(f"Back on login page: {chk_back.get('result', {}).get('result', {}).get('value')}")

    finally:
        proc.terminate()

asyncio.run(test())
