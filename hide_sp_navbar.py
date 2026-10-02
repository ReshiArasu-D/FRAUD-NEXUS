import requests, os
from dotenv import load_dotenv
load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

page_id = 'e4358577c32b43d0e54832f1b40131d0'
r = requests.patch(
    f'{url}/api/now/table/sp_page/{page_id}',
    auth=auth, headers=headers,
    json={'css': 'header[role="banner"], .sp-page-root > header, #sp-nav-bar, .navbar-default { display: none !important; }'}
)
print('Updated sp_page.css status:', r.status_code)
