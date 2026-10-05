import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--disable-gpu', '--remote-debugging-port=9299', '--user-data-dir=d:\KPMG\.edge_temp_profile_btncheck', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r = requests.put('http://localhost:9299/json/new?about:blank').json()
        async with websockets.connect(r['webSocketDebuggerUrl']) as ws:
            async def cmd(m, p={}):
                await ws.send(json.dumps({'id': 1, 'method': m, 'params': p}))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('id') == 1: return res.get('result', {})
            await cmd('Page.enable')
            await cmd('Runtime.enable')
            await cmd('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(6)
            
            # Find all buttons and links
            res = await cmd('Runtime.evaluate', {
                'expression': 'JSON.stringify(Array.from(document.querySelectorAll("button, a")).map(b => ({tag: b.tagName, text: b.innerText, cls: b.className, onclick: b.getAttribute("ng-click") || b.getAttribute("onclick")})))',
                'returnByValue': True
            })
            print('Interactive Elements:\n', res.get('result', {}).get('value'))
    finally: proc.terminate()

asyncio.run(test())
