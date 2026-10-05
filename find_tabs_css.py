import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
css = r.json()['result'].get('css', '')

print(f"Total CSS length: {len(css)}")

# Search for any rules matching tabs
for term in [".fnx-auth-tabs", "auth-tabs", "tabs"]:
    idx = css.find(term)
    print(f"=== Searching for '{term}' ===")
    count = 0
    while idx != -1:
        # print the rule block
        b_start = css.rfind("{", 0, idx)
        rule_start = css.rfind("}", 0, b_start)
        if rule_start == -1: rule_start = 0
        rule_end = css.find("}", idx)
        
        snippet = css[rule_start:rule_end+1].strip()
        if "height" in snippet or "overflow" in snippet:
            print(f"[{idx}] Found with height/overflow:")
            print(snippet)
            print("-" * 30)
            count += 1
        idx = css.find(term, idx+1)
    print(f"Total occurrences of '{term}' with height/overflow: {count}")
