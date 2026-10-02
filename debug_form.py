import requests, os, re, urllib.parse
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')

s = requests.Session()
login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
s.get(login_url)

r_form = s.get(f"{url}/sys_db_object.do?sys_id=-1")
g_ck_match = re.search(r'g_ck\s*=\s*["\']([^"\']+)["\']', r_form.text)
g_ck = g_ck_match.group(1) if g_ck_match else ""

print("Form response status:", r_form.status_code)
print("g_ck:", g_ck)

# Check all fields in the actual form
fields = {}
for m in re.finditer(r'name=["\']([^"\']+)["\'](?:\s+value=["\']([^"\']*)["\'])?', r_form.text):
    name = m.group(1)
    val = m.group(2) if m.group(2) is not None else ""
    fields[name] = val

print("Fields found:", len(fields))
for k, v in list(fields.items())[:25]:
    print(f" {k} = {v}")
