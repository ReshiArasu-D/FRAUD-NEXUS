import asyncio
import subprocess
import requests
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9258',
        '--no-first-run', '--no-default-browser-check',
        '--window-size=1280,1000',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile34',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9258/json/new?about:blank')
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

            script = """
            (() => {
                const results = [];
                const all = Array.from(document.querySelectorAll('*'));
                for (let el of all) {
                    const txt = el.innerText || '';
                    if (txt.trim() === 'Log in' || txt.trim() === 'servicenow' || txt.includes('Log in')) {
                        results.push({
                            tag: el.tagName,
                            id: el.id,
                            className: el.className,
                            parentTag: el.parentElement?.tagName,
                            parentClass: el.parentElement?.className,
                            grandParentTag: el.parentElement?.parentElement?.tagName,
                            grandParentClass: el.parentElement?.parentElement?.className,
                            text: txt.substring(0, 50)
                        });
                    }
                }
                return JSON.stringify(results.slice(0, 15));
            })()
            """
            res = await send('Runtime.evaluate', {'expression': script, 'returnByValue': True})
            print("Login elements found:\n", res['result']['result'].get('value'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
