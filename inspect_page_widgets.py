import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9239',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile15', 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9239/json/new?about:blank')
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
                        return m.get('result', {})

            await send('Page.enable')
            await send('Runtime.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)

            script = """
            (() => {
                const widgets = Array.from(document.querySelectorAll('[widget], sp-widget, div[ng-include], div[widget]')).map(w => ({
                    tag: w.tagName,
                    widgetAttr: w.getAttribute('widget'),
                    html: w.outerHTML.substring(0, 300)
                }));
                const errors = Array.from(document.querySelectorAll('.alert, .has-error, .text-danger')).map(e => e.innerText);
                return JSON.stringify({
                    widgets: widgets,
                    errors: errors,
                    mainWrapperHTML: document.getElementById('sp-main-wrapper')?.innerHTML?.substring(0, 1500)
                });
            })()
            """
            res = await send('Runtime.evaluate', {'expression': script, 'returnByValue': True})
            print('Inspect Widgets & Main Wrapper:\n', res.get('result', {}).get('value'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
