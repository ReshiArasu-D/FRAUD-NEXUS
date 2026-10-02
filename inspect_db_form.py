import requests
import os
import re
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')

s = requests.Session()
login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
s.get(login_url)

r = s.get(f"{url}/sys_db_object.do?sys_id=-1")
print("sys_db_object.do form status:", r.status_code)
# Search for input fields
inputs = re.findall(r'<input[^>]+name=["\']([^"\']+)["\'][^>]*>', r.text)
print("Input names count:", len(inputs))
print("Sample inputs:", inputs[:20])

g_ck = re.search(r'g_ck\s*=\s*["\']([^"\']+)["\']', r.text)
if g_ck:
    print("Found g_ck:", g_ck.group(1))
