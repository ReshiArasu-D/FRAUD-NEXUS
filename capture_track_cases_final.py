import asyncio, json, requests, websockets, base64

async def run():
    resp = requests.get('http://127.0.0.1:9222/json')
    target = next(t for t in resp.json() if 'fnx' in t.get('url', ''))
    async with websockets.connect(target['webSocketDebuggerUrl']) as ws:
        msg = {'id': 1, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}
        await ws.send(json.dumps(msg))
        res = json.loads(await ws.recv())
        with open('d:/KPMG/track_cases_view_buttons_final.png', 'wb') as f:
            f.write(base64.b64decode(res['result']['data']))

asyncio.run(run())
print('Captured d:/KPMG/track_cases_view_buttons_final.png')
