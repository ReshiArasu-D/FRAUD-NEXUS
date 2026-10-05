import asyncio, json, requests, websockets

async def run():
    resp = requests.get('http://127.0.0.1:9222/json')
    target = next(t for t in resp.json() if 'fnx' in t.get('url', ''))
    async with websockets.connect(target['webSocketDebuggerUrl']) as ws:
        msg = {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': """
            (() => {
                const scope = angular.element(document.querySelector('.fnx-app')).scope();
                scope.c.selectedCase = null;
                scope.$apply();
            })()
        """}}
        await ws.send(json.dumps(msg))
        await ws.recv()

asyncio.run(run())
print('Reset to Track Cases list successfully')
