import requests, os
from dotenv import load_dotenv
load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json'}
r = requests.get(f'{url}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f', auth=auth, headers=headers)
t = r.json()['result']['template']
print('Current Template Length on ServiceNow:', len(t))
print('Has <style>:', '<style>' in t)
print('Has {{icon:', '{{icon:' in t)
print('Has ng-class="{{:', 'ng-class="{{' in t)
