import requests, os, re, urllib.parse, time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')
auth = HTTPBasicAuth(user, pwd)

def create_table_via_form(label: str, name_suffix: str, extends_task: bool = False):
    # Check if already exists
    r_check = requests.get(f"{url}/api/now/table/sys_db_object?sysparm_query=nameLIKE{name_suffix}&sysparm_fields=name,label,sys_id", auth=auth)
    res = r_check.json().get('result', [])
    if res:
        print(f"Table '{label}' ({name_suffix}) already exists: {res[0]['name']} ({res[0]['sys_id']})")
        return res[0]

    s = requests.Session()
    login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
    s.get(login_url)

    r_form = s.get(f"{url}/sys_db_object.do?sys_id=-1")
    g_ck_match = re.search(r'g_ck\s*=\s*["\']([^"\']+)["\']', r_form.text)
    g_ck = g_ck_match.group(1) if g_ck_match else ""

    fields = {}
    for m in re.finditer(r'<input[^>]+name=["\']([^"\']+)["\'][^>]*>', r_form.text):
        tag = m.group(0)
        name_m = re.search(r'name=["\']([^"\']+)["\']', tag)
        val_m = re.search(r'value=["\']([^"\']*)["\']', tag)
        if name_m:
            fields[name_m.group(1)] = val_m.group(1) if val_m else ""

    fields['sys_action'] = 'sysverb_insert'
    fields['sysparm_ck'] = g_ck
    fields['sys_db_object.label'] = label
    fields['sys_db_object.name'] = name_suffix
    fields['sys_db_object.create_access_controls'] = 'true'
    fields['sys_db_object.access'] = 'public'
    
    if extends_task:
        fields['sys_db_object.super_class'] = '06ff39c5c3530310e54832f1b40131f5' # Task sys_id
        fields['sys_display.sys_db_object.super_class'] = 'Task'

    headers = {
        'Referer': f"{url}/sys_db_object.do?sys_id=-1",
        'Origin': url
    }
    r_post = s.post(f"{url}/sys_db_object.do", data=fields, headers=headers)
    print(f"Submitted '{label}' -> HTTP {r_post.status_code}")
    
    time.sleep(4)
    r_check = requests.get(f"{url}/api/now/table/sys_db_object?sysparm_query=nameLIKE{name_suffix}&sysparm_fields=name,label,sys_id", auth=auth)
    res = r_check.json().get('result', [])
    print(f"Verified '{label}':", res)
    return res[0] if res else None

tables_to_create = [
    ("Fraud Evidence", "x_fnx_evidence", False),
    ("Evidence Custody Log", "x_fnx_custody_log", False),
    ("FRAUDNEXUS Audit Log", "x_fnx_audit", False)
]

for label, suffix, ext in tables_to_create:
    create_table_via_form(label, suffix, ext)
    time.sleep(2)
