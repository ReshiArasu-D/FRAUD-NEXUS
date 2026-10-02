import asyncio
import subprocess
import requests
import json

async def test():
    proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', '--remote-debugging-port=9244',
        r'--user-data-dir=d:\KPMG\.edge_temp_profile20',
        'https://dev187180.service-now.com/fnx'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(4)
        targets = requests.get('http://localhost:9244/json/list').json()
        print("Targets after direct launch:")
        for t in targets:
            print(" ", t.get('type'), t.get('title'), t.get('url'))
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(test())
