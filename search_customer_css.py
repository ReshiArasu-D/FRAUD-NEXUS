import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
css = r.json()['result'].get('css', '')

for target in ['.fnx-track-cases', '.fnx-evidence-vault', '.fnx-help-view', '.fnx-content', '.fnx-ai-widget', '.fnx-ai-trigger', '.fnx-dashboard']:
    print(f"=== SEARCH FOR: {target} ===")
    idx = css.find(target)
    count = 0
    while idx != -1:
        # print snippet
        start = max(0, idx - 50)
        end = min(len(css), idx + 200)
        print(f"[{idx}]", css[start:end])
        print("-" * 20)
        count += 1
        idx = css.find(target, idx + 1)
    if count == 0:
        print("NOT FOUND IN CSS")
