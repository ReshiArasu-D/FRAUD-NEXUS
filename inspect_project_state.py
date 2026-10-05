import os, sys, re, requests

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=== INSPECTING CURRENT SERVICENOW WIDGET ===")
try:
    r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
    if r.status_code == 200:
        res = r.json()['result']
        tpl = res.get('template', '')
        cs = res.get('client_script', '')
        css = res.get('css', '')
        print(f"Widget Name: {res.get('name')}")
        print(f"Template length: {len(tpl)}")
        print(f"Client script length: {len(cs)}")
        print(f"CSS length: {len(css)}")
        
        views = set(re.findall(r"c\.currentView\s*===?\s*'([^']+)'", tpl))
        admin_sections = set(re.findall(r"c\.adminSection\s*===?\s*'([^']+)'", tpl))
        tabs = set(re.findall(r"c\.\w*[Tt]ab\s*===?\s*'([^']+)'", tpl))
        print("Views in template:", sorted(list(views)))
        print("Admin sections in template:", sorted(list(admin_sections)))
        print("Tabs in template:", sorted(list(tabs)))
    else:
        print(f"Error fetching widget: {r.status_code} - {r.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")

print("\n=== INSPECTING LOCAL ADMIN FILES ===")
if os.path.exists('d:/KPMG/admin'):
    print("Files in d:/KPMG/admin:", os.listdir('d:/KPMG/admin'))

if os.path.exists('d:/KPMG/admin_template.html'):
    adm_tpl = open('d:/KPMG/admin_template.html', 'r', encoding='utf-8').read()
    print(f"admin_template.html size: {len(adm_tpl)}")
    adm_views = set(re.findall(r"c\.adminSection\s*===?\s*'([^']+)'", adm_tpl))
    print("Admin sections in admin_template.html:", sorted(list(adm_views)))

print("\n=== INSPECTING SERVICENOW CUSTOM TABLES ===")
try:
    r = requests.get(f'{base}/api/now/table/sys_db_object?sysparm_query=nameSTARTSWITHx_fraudnexus&sysparm_fields=name,label', auth=auth, headers={'Accept':'application/json'})
    if r.status_code == 200:
        tables = r.json().get('result', [])
        print(f"Found {len(tables)} x_fraudnexus tables:")
        for t in tables:
            print(f" - {t.get('name')}: {t.get('label')}")
    else:
        print(f"Tables query status: {r.status_code}")
except Exception as e:
    print(f"Exception checking tables: {e}")
