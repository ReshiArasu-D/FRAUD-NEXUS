import asyncio
import subprocess
import requests
import json
import websockets

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9249',
        '--no-first-run', '--no-default-browser-check',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile25',
        'https://dev187180.service-now.com/fnx'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(6)
        targets = requests.get('http://localhost:9249/json/list').json()
        target = next((t for t in targets if 'dev187180.service-now.com/fnx' in t.get('url', '')), None)
        ws_url = target.get('webSocketDebuggerUrl')
        async with websockets.connect(ws_url) as ws:
            expr = """
            (() => {
                const root = angular.element(document.querySelector('[ng-app]') || document.body).scope();
                if (!root) return 'NO_ROOT_SCOPE';
                return JSON.stringify({
                    portal: root.portal ? root.portal.title : null,
                    page: root.page ? root.page.title : null,
                    containersCount: root.containers ? root.containers.length : null,
                    mainFirstPage: root.main ? root.main.firstPage : null,
                    user: root.user ? root.user.name : null
                });
            })()
            """
            cmd = {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}
            await ws.send(json.dumps(cmd))
            res = json.loads(await ws.recv())
            print('Scope State:', res['result']['result'].get('value'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
