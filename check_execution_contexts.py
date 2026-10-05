import asyncio, subprocess, requests, json, websockets, sys

sys.stdout.reconfigure(encoding='utf-8')

async def test():
    proc = subprocess.Popen([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--disable-gpu', '--remote-debugging-port=9301', r'--user-data-dir=d:\KPMG\.edge_temp_profile_ctxcheck', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        r = requests.put('http://localhost:9301/json/new?about:blank').json()
        async with websockets.connect(r['webSocketDebuggerUrl']) as ws:
            contexts = []
            msg_id = 1
            async def send(m, p={}):
                nonlocal msg_id
                mid = msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': mid, 'method': m, 'params': p}))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('method') == 'Runtime.executionContextCreated':
                        contexts.append(res['params']['context'])
                    if res.get('id') == mid:
                        return res.get('result', {})

            await send('Page.enable')
            await send('Runtime.enable')
            await send('Page.navigate', {'url': 'https://dev187180.service-now.com/fnx'})
            await asyncio.sleep(7)
            
            print('Contexts detected:', len(contexts))
            for ctx in contexts:
                print(' - Context ID:', ctx['id'], 'Name:', ctx.get('name'), 'Origin:', ctx.get('origin'))
                # Evaluate in that specific context
                try:
                    res = await send('Runtime.evaluate', {
                        'expression': 'JSON.stringify({url: window.location.href, buttons: Array.from(document.querySelectorAll("button")).map(b => b.innerText)})',
                        'contextId': ctx['id'],
                        'returnByValue': True
                    })
                    print('   Result:', res.get('result', {}).get('value'))
                except Exception as ex:
                    print('   Error evaluating in ctx:', ex)
    finally: proc.terminate()

asyncio.run(test())
