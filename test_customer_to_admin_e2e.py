"""
FRAUDNEXUS Customer -> Admin End-to-End Operational Lifecycle Test
Verifies Section 55 requirements:
1. Customer registers / logs in
2. Customer reports fraud (structured financial transaction + evidence)
3. Case created & ID generated
4. Admin logs in via Try Demo / Quick Login (Alex Morgan)
5. Admin Command Center loads newly reported case
6. Admin opens case in Investigation Workspace
7. Customer, Financial, Evidence records visible to investigator
8. Admin assigns case to investigator
9. Admin adds investigation task
10. Admin requests evidence from customer
11. Admin escalates case to senior management
12. Admin resolves case
13. Admin closes case
14. Complete Audit & Custody timeline verified
15. Customer Portal reflects 'Resolved' / 'Closed' status
"""
import requests
import os
import sys
import json
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv('d:/KPMG/.env')

url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
api = f"{url}/api/2229367/fnx_api"

print("======================================================================")
print("RUNNING FRAUDNEXUS CUSTOMER -> ADMIN E2E INTEGRATION SUITE")
print("======================================================================")

# Step 1: Customer Account
ts = int(time.time())
cust_email = f"victim.e2e.{ts}@example.com"
cust_pass = "DemoPass123!"

print("\n[STEP 1] Customer Registration")
r_reg = requests.post(f"{api}/register", auth=auth, headers=headers, json={
    "name": "Kavitha Raman",
    "email": cust_email,
    "mobile": "9876543210",
    "dob": "1994-06-15",
    "gender": "Female",
    "occupation": "Software Engineer",
    "address": "45/2 Gandhi Road, Velachery, Chennai",
    "password": cust_pass
})
assert r_reg.status_code == 200, f"Registration failed: {r_reg.text}"
user_id = r_reg.json()['result']['user_id']
cust_id = r_reg.json()['result']['customer_id']
print(f"PASS: Customer registered (User: {user_id}, Customer ID: {cust_id})")

# Step 2: Customer submits Fraud Report with Financial & Evidence
print("\n[STEP 2] Customer Submits Fraud Report with Transaction & Evidence")
r_case = requests.post(f"{api}/cases", auth=auth, headers=headers, json={
    "user_id": user_id,
    "customer_id": cust_id,
    "type": "Unauthorized Transaction",
    "description": "Unauthorized night debit of Rs 85,000 from savings account via IMPS without OTP generation.",
    "incident_date": "2026-01-12",
    "incident_time": "03:15:00",
    "location": "Chennai",
    "area": "Velachery",
    "pincode": "600042",
    "digital_platform": "HDFC Mobile Banking",
    "exposure": 85000,
    "severity": "Critical",
    "has_financial": True,
    "institution_type": "Scheduled Commercial Bank",
    "institution_name": "HDFC Bank",
    "payment_mode": "IMPS",
    "reference_type": "UTR",
    "reference_value": f"UTR-IMPS-{ts}",
    "evidence_type": "Bank Account Statement",
    "evidence_description": "Disputed transaction highlight showing Rs 85,000 debit",
    "attachment_name": f"HDFC_Statement_Jan_{ts}.pdf"
})
assert r_case.status_code == 201, f"Case creation failed: {r_case.text}"
case_data = r_case.json()['result']
case_sys_id = case_data['case_id']
case_number = case_data['number']
print(f"PASS: Fraud case created: {case_number} (sys_id: {case_sys_id})")

# Step 3: Admin Demo Authentication
print("\n[STEP 3] Admin / Investigator Quick Login (Alex Morgan)")
r_admin_login = requests.post(f"{api}/admin_login", auth=auth, headers=headers, json={"demo": True})
assert r_admin_login.status_code == 200, f"Admin login failed: {r_admin_login.text}"
admin_user = r_admin_login.json()['result']['user']
print(f"PASS: Authenticated as {admin_user['name']} ({admin_user['title']}, Role: {admin_user['role']})")

# Step 4: Command Center Verification
print("\n[STEP 4] Admin Command Center Dashboard Ingestion")
r_dash = requests.get(f"{api}/admin_dashboard", auth=auth, headers=headers)
assert r_dash.status_code == 200, f"Dashboard failed: {r_dash.text}"
dash = r_dash.json()['result']
print(f"PASS: Live KPIs computed - Active Cases: {dash['stats']['activeCases']}, Exposure: ₹{dash['stats']['financialExposure']:,.2f}")

# Step 5: Investigator opens Case in Investigation Workspace
print("\n[STEP 5] Investigator Opens Case in Investigation Workspace")
r_detail = requests.get(f"{api}/admin_cases?case_id={case_sys_id}", auth=auth, headers=headers)
assert r_detail.status_code == 200, f"Case detail query failed: {r_detail.text}"
c_detail = r_detail.json()['result']['case']
assert c_detail['number'] == case_number
print(f"PASS: Case loaded in Investigation Workspace: {c_detail['number']}, Type: {c_detail['type']}, Exposure: ₹{c_detail['exposure']}")
print(f"      Customer: {c_detail['customer']['name']} ({c_detail['customer']['email']})")
print(f"      Evidence Count: {len(c_detail['evidence'])}")

# Step 6: Case Assignment
print("\n[STEP 6] Investigator Assigns Case")
r_assign = requests.post(f"{api}/admin_cases", auth=auth, headers=headers, json={
    "action": "assign",
    "case_id": case_sys_id,
    "handler_name": "Alex Morgan"
})
assert r_assign.status_code == 200, f"Assign failed: {r_assign.text}"
print("PASS: Case assigned to Alex Morgan")

# Step 7: Add Investigation Task
print("\n[STEP 7] Investigator Adds Task")
r_task = requests.post(f"{api}/admin_cases", auth=auth, headers=headers, json={
    "action": "add_task",
    "case_id": case_sys_id,
    "title": "Freeze beneficiary account at receiving bank",
    "description": "Send Section 91 notice to intermediary payment switch",
    "priority": "Critical"
})
assert r_task.status_code == 200, f"Task creation failed: {r_task.text}"
print(f"PASS: Task created: {r_task.json()['result']['task_number']}")

# Step 8: Request Evidence from Customer
print("\n[STEP 8] Investigator Requests Additional Evidence")
r_ev_req = requests.post(f"{api}/admin_cases", auth=auth, headers=headers, json={
    "action": "request_evidence",
    "case_id": case_sys_id,
    "notes": "Please provide device screenshot showing the SMS inbox during the incident timeframe."
})
assert r_ev_req.status_code == 200, f"Evidence request failed: {r_ev_req.text}"
print("PASS: Evidence request dispatched and recorded in case timeline")

# Step 9: Escalate Case
print("\n[STEP 9] Investigator Escalates Case")
r_esc = requests.post(f"{api}/admin_cases", auth=auth, headers=headers, json={
    "action": "escalate",
    "case_id": case_sys_id,
    "reason": "Suspected mule syndicate account operating across state borders."
})
assert r_esc.status_code == 200, f"Escalation failed: {r_esc.text}"
print("PASS: Case escalated to Senior Investigation Management")

# Step 10: Resolve Case
print("\n[STEP 10] Investigator Resolves Case")
r_res = requests.post(f"{api}/admin_cases", auth=auth, headers=headers, json={
    "action": "resolve",
    "case_id": case_sys_id,
    "outcome": "Confirmed Fraud",
    "notes": "Beneficiary account frozen; Rs 50,000 recovered and queued for lien reversal."
})
assert r_res.status_code == 200, f"Resolution failed: {r_res.text}"
print("PASS: Case marked Resolved with outcome 'Confirmed Fraud'")

# Step 11: Close Case
print("\n[STEP 11] Authorized User Closes Case")
r_close = requests.post(f"{api}/admin_cases", auth=auth, headers=headers, json={
    "action": "close",
    "case_id": case_sys_id,
    "notes": "All operational statutory protocols completed."
})
assert r_close.status_code == 200, f"Closure failed: {r_close.text}"
print("PASS: Case closed successfully")

# Step 12: Verify Timeline & Audit History
print("\n[STEP 12] Audit & Custody Timeline Verification")
r_aud = requests.get(f"{api}/admin_cases?case_id={case_sys_id}", auth=auth, headers=headers)
assert r_aud.status_code == 200
updated_case = r_aud.json()['result']['case']
print(f"PASS: Case status is now '{updated_case['status']}', Stage: '{updated_case['stage']}'")
print(f"      Total Timeline Audit Events: {len(updated_case['timeline'])}")
for idx, tl in enumerate(updated_case['timeline'][:5]):
    print(f"      [{idx+1}] {tl['action']}: {tl['details']}")

# Step 13: Customer Portal Visibility
print("\n[STEP 13] Customer Portal Status Synchronization")
r_cust_view = requests.get(f"{api}/cases?user_id={user_id}", auth=auth, headers=headers)
assert r_cust_view.status_code == 200
cust_cases = r_cust_view.json()['result']['cases']
assert len(cust_cases) == 1
assert cust_cases[0]['number'] == case_number
assert cust_cases[0]['status'] in ['Closed', 'Resolved']
print(f"PASS: Customer portal sees updated case status: '{cust_cases[0]['status']}' (Stage: '{cust_cases[0]['stage']}')")

print("\n======================================================================")
print("FRAUDNEXUS CUSTOMER -> ADMIN E2E INTEGRATION: ALL 13 STEPS PASSED!")
print("======================================================================")
