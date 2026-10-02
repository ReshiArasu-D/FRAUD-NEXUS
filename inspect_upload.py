import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
s = requests.Session()
s.get(f'{url}/login.do?user_name=admin&sys_action=sysverb_login&user_password=mn%25XC1%5EScdA4')
r = s.get(f'{url}/upload.do')

for m in re.finditer(r'<input[^>]+>', r.text):
    print(m.group(0))
for m in re.finditer(r'<form[^>]+>', r.text):
    print(m.group(0))
