import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
s = requests.Session()
s.auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
r = s.get(f"{url}/sys.scripts.do")
print("Status:", r.status_code)
print("Length:", len(r.text))
print("First 800 chars:\n", r.text[:800])
