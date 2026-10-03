import requests
import os
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
base = f"{url}/api/2229367/fnx_api"

print("--- 1. Testing Demo Admin Login ---")
r_login = requests.post(f"{base}/admin_login", auth=auth, headers=headers, json={"demo": True})
print("Login Status:", r_login.status_code)
print("Login Body:", json.dumps(r_login.json(), indent=2))

print("\n--- 2. Testing Admin Dashboard ---")
r_dash = requests.get(f"{base}/admin_dashboard", auth=auth, headers=headers)
print("Dash Status:", r_dash.status_code)
dash_data = r_dash.json().get('result', {})
print("KPI Stats:", json.dumps(dash_data.get('stats'), indent=2))
print("Priority Queue Count:", len(dash_data.get('priority_queue', [])))
print("Action Center Count:", len(dash_data.get('action_center', [])))
print("Recent Activity Count:", len(dash_data.get('recent_activity', [])))

print("\n--- 3. Testing Admin Cases List ---")
r_cases = requests.get(f"{base}/admin_cases?filter=all", auth=auth, headers=headers)
print("Cases Status:", r_cases.status_code)
cases_data = r_cases.json().get('result', {})
print("Cases Count:", cases_data.get('count'))

print("\n--- 4. Testing Admin Customers List ---")
r_cust = requests.get(f"{base}/admin_customers", auth=auth, headers=headers)
print("Customers Status:", r_cust.status_code)
cust_data = r_cust.json().get('result', {})
print("Customers Count:", cust_data.get('count'))

print("\n--- 5. Testing Admin AI ---")
r_ai = requests.post(f"{base}/admin_ai", auth=auth, headers=headers, json={"query": "How many critical cases are open?"})
print("AI Status:", r_ai.status_code)
print("AI Reply:", json.dumps(r_ai.json().get('result'), indent=2))
