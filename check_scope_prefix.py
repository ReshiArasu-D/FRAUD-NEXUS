import requests
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')

s = requests.Session()
login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
s.get(login_url)

# Check concoursepicker application
r = s.get(f"{url}/api/now/ui/concoursepicker/application")
print("Current app picker:", r.json())

# Switch app to FRAUDNEXUS (b4617cbfc32743d0e54832f1b40131f8)
r_switch = s.put(f"{url}/api/now/ui/concoursepicker/application", json={"app_id": "b4617cbfc32743d0e54832f1b40131f8"})
print("Switch app status:", r_switch.status_code, r_switch.text)

# Check sys_db_object.do form to see what prefix it gives
r_form = s.get(f"{url}/sys_db_object.do?sys_id=-1")
import re
prefix_match = re.search(r'id=["\']sys_db_object\.name["\'][^>]*', r_form.text)
print("Name field html:", prefix_match.group(0) if prefix_match else "Not found")
# Look for prefix text or span
for m in re.finditer(r'<span[^>]*class=["\'][^"\']*prefix[^"\']*["\'][^>]*>(.*?)</span>', r_form.text, re.IGNORECASE):
    print("Found prefix span:", m.group(0))
