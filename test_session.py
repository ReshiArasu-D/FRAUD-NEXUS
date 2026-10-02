import requests
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
user = os.getenv('SERVICENOW_USERNAME')
pwd = os.getenv('SERVICENOW_PASSWORD')

s = requests.Session()
# Login via login.do
login_url = f"{url}/login.do?user_name={urllib.parse.quote(user)}&sys_action=sysverb_login&user_password={urllib.parse.quote(pwd)}"
r_login = s.get(login_url)
print("Login status:", r_login.status_code)
print("Cookies:", s.cookies.get_dict())

# Check /navpage.do
r_nav = s.get(f"{url}/navpage.do")
print("Navpage status:", r_nav.status_code)
if "admin" in r_nav.text:
    print("Logged in as admin successfully!")
