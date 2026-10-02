import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9241',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile17', 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r_new = requests.put('http://localhost:9241/json/new?about:blank')
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
            await asyncio.sleep(7)

            # Dump DOM structure
            script = """
            (() => {
                function serializeNode(el, depth = 0) {
                    if (depth > 6 || !el) return '';
                    let str = '  '.repeat(depth) + el.tagName + (el.className ? '.' + el.className.split(' ').join('.') : '') + (el.id ? '#' + el.id : '') + '\\n';
                    for (let child of el.children) {
                        str += serializeNode(child, depth + 1);
                    }
                    return str;
                }
                const root = document.getElementById('sp-main-wrapper') || document.body;
                return serializeNode(root);
            })()
            """
            res = await send('Runtime.evaluate', {'expression': script, 'returnByValue': True})
            tree = res.get('result', {}).get('value', '')
            print("DOM Tree:\n", tree[:2500])
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
