import json, requests, websocket

# Find browser target
resp = requests.get('http://127.0.0.1:9222/json')
targets = resp.json()
print("Found targets:", len(targets))

target = None
for t in targets:
    if 'dev187180.service-now.com/fnx' in t.get('url', ''):
        target = t
        break

if not target:
    print("FNX target not found! Targets are:")
    for t in targets:
        print(t.get('title'), t.get('url'))
    exit(1)

ws_url = target['webSocketDebuggerUrl']
ws = websocket.create_connection(ws_url)

def cdp_eval(expr):
    msg = json.dumps({
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expr,
            "returnByValue": True
        }
    })
    ws.send(msg)
    res = json.loads(ws.recv())
    return res.get('result', {}).get('result', {}).get('value')

print("Page URL:", cdp_eval("window.location.href"))

# Inspect Angular scope
check_script = """
(() => {
    const el = document.querySelector('.fnx-app') || document.querySelector('[ng-controller]');
    if (!el) return 'No angular element found';
    const scope = angular.element(el).scope();
    const c = scope.c;
    return {
        currentView: c.currentView,
        sidebarItems: Array.from(document.querySelectorAll('.fnx-nav-item')).map(a => ({
            text: a.innerText.trim(),
            classes: a.className,
            clickAttr: a.getAttribute('ng-click'),
            ngClassAttr: a.getAttribute('ng-class')
        })),
        evidenceVaultVisible: !!document.querySelector('.fnx-evidence-vault'),
        helpViewVisible: !!document.querySelector('.fnx-help-view')
    };
})()
"""

info = cdp_eval(check_script)
print("DOM & Angular Info:")
print(json.dumps(info, indent=2))

ws.close()
