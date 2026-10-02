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

r = s.get(f"{url}/sys.scripts.do")
print(r.text)
