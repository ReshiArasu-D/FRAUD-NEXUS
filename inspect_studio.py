import requests, os, re
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
s = requests.Session()
s.get(f'{url}/login.do?user_name=admin&sys_action=sysverb_login&user_password=mn%25XC1%5EScdA4')
r = s.get(f'{url}/$studio.do?sysparm_app_id=b4617cbfc32743d0e54832f1b40131f8')

# Search for api endpoints in studio
apis = re.findall(r'api/now/[a-zA-Z0-9_\/]+', r.text)
print("Studio APIs found:", set(apis))

# Also search for studio specific urls
studio_urls = re.findall(r'[\'"][^\'"]*studio[^\'"]*[\'"]', r.text, re.IGNORECASE)
print("Studio URLs:", set(studio_urls[:10]))
