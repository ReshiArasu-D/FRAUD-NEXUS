import requests
import os
import re
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')

def execute_background_script(script: str, scope="global"):
    s = requests.Session()
    # Use headers
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
    r_log = s.get(login_url)
    
    r_form = s.get(f"{url}/sys.scripts.do")
    
    # Try multiple regex patterns
    ck_match = re.search(r'name=["\']sysparm_ck["\'][^>]*value=["\']([^"\']+)["\']', r_form.text)
    if not ck_match:
        ck_match = re.search(r'value=["\']([^"\']+)["\'][^>]*name=["\']sysparm_ck["\']', r_form.text)
    if not ck_match:
        ck_match = re.search(r'g_ck\s*=\s*["\']([^"\']+)["\']', r_form.text)
        
    if not ck_match:
        print("HTML snippet:\n", r_form.text[:1000])
        raise ValueError("Could not extract sysparm_ck from sys.scripts.do")
    
    sysparm_ck = ck_match.group(1)
    
    post_data = {
        "script": script,
        "sysparm_ck": sysparm_ck,
        "runscript": "Run script",
        "sys_scope": scope,
        "record_for_rollback": "on",
        "quota_managed_transaction": "on"
    }
    
    r_exec = s.post(f"{url}/sys.scripts.do", data=post_data)
    
    # Extract output from <pre> tags or clean HTML
    clean_out = re.sub(r'<[^>]+>', '', r_exec.text)
    return clean_out.strip()

test_script = """
gs.print('--- TEST SCRIPT EXECUTION ---');
var tc = new GlideTableCreator('x_fnx_customer', 'FRAUDNEXUS Customer');
tc.setScope('x_fnx_fraudnexus');
tc.create();
gs.print('Created x_fnx_customer table!');
"""

output = execute_background_script(test_script)
print("Output:\n", output)
