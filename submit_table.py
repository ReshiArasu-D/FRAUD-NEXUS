import requests, os, re, urllib.parse
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')
auth = HTTPBasicAuth(user, pwd)

def create_table_via_form(label: str, name_suffix: str, extends_task: bool = False):
    s = requests.Session()
    login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
    s.get(login_url)

    # 1. GET sys_db_object.do?sys_id=-1
    r_form = s.get(f"{url}/sys_db_object.do?sys_id=-1")
    
    # 2. Extract g_ck
    g_ck_match = re.search(r'g_ck\s*=\s*["\']([^"\']+)["\']', r_form.text)
    g_ck = g_ck_match.group(1) if g_ck_match else ""

    # 3. Extract all input fields
    fields = {}
    for m in re.finditer(r'<input[^>]+name=["\']([^"\']+)["\'][^>]*>', r_form.text):
        tag = m.group(0)
        name_m = re.search(r'name=["\']([^"\']+)["\']', tag)
        val_m = re.search(r'value=["\']([^"\']*)["\']', tag)
        if name_m:
            fields[name_m.group(1)] = val_m.group(1) if val_m else ""

    # 4. Fill custom table data
    fields['sys_action'] = 'sysverb_insert'
    fields['sysparm_ck'] = g_ck
    fields['sys_db_object.label'] = label
    fields['sys_db_object.name'] = name_suffix
    fields['sys_db_object.create_access_controls'] = 'true'
    fields['sys_db_object.access'] = 'public'
    
    if extends_task:
        fields['sys_db_object.super_class'] = '06ff39c5c3530310e54832f1b40131f5' # Task sys_id
        fields['sys_display.sys_db_object.super_class'] = 'Task'

    # 5. POST form
    headers = {
        'Referer': f"{url}/sys_db_object.do?sys_id=-1",
        'Origin': url
    }
    r_post = s.post(f"{url}/sys_db_object.do", data=fields, headers=headers)
    print(f"Submitted '{label}' -> HTTP {r_post.status_code}")
    
    # 6. Verify table exists via Table API
    r_check = requests.get(f"{url}/api/now/table/sys_db_object?sysparm_query=label={urllib.parse.quote(label)}^ORnameLIKE{name_suffix}&sysparm_fields=name,label,sys_id", auth=auth)
    res = r_check.json().get('result', [])
    print(f"Verification for '{label}':", res)
    return res

if __name__ == "__main__":
    create_table_via_form("Fraud Case", "x_fnx_case", extends_task=True)
