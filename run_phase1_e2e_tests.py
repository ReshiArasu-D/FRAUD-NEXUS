import requests
import json
import os
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
admin_auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
API_BASE = f"{url}/api/2229367/fnx_api"

test_results = {}

def run_test(test_id, test_name, func):
    print(f"\n========================================================")
    print(f"RUNNING: [{test_id}] {test_name}")
    print(f"========================================================")
    try:
        success, details = func()
        status = "PASS" if success else "FAIL"
        test_results[test_id] = {"name": test_name, "status": status, "details": details}
        print(f"RESULT: [{status}] - {details}")
        return success
    except Exception as e:
        test_results[test_id] = {"name": test_name, "status": "FAIL", "details": str(e)}
        print(f"RESULT: [FAIL] Exception: {e}")
        return False

# Setup test variables with timestamp to avoid duplicates across test runs
ts = int(time.time())
cust1_email = f"arun.fnx.{ts}@example.com"
cust1_name = "Arun Kumar"
cust1_mobile = "9000000001"
cust1_pass = "DemoPass123!"

cust2_email = f"priya.fnx.{ts}@example.com"
cust2_name = "Priya Sharma"
cust2_mobile = "9000000002"
cust2_pass = "DemoPass123!"

state = {}

# ----------------------------------------------------
# TEST 001: Customer Registration
# ----------------------------------------------------
def t001():
    payload = {
        "name": cust1_name,
        "email": cust1_email,
        "mobile": cust1_mobile,
        "password": cust1_pass
    }
    r = requests.post(f"{API_BASE}/register", headers=headers, json=payload, timeout=20)
    data = r.json().get('result', r.json())
    if r.status_code == 200 and data.get('success'):
        state['user1_id'] = data['user_id']
        state['cust1_id'] = data['customer_id']
        
        # Verify in ServiceNow sys_user
        r_u = requests.get(f"{url}/api/now/table/sys_user/{state['user1_id']}", auth=admin_auth, headers=headers)
        user_exists = (r_u.status_code == 200)
        
        # Verify in ServiceNow u_x_fnx_customer
        r_c = requests.get(f"{url}/api/now/table/u_x_fnx_customer?sysparm_query=u_user={state['user1_id']}", auth=admin_auth, headers=headers)
        cust_records = r_c.json().get('result', [])
        cust_exists = (len(cust_records) > 0)
        if cust_exists:
            state['customer1_sys_id'] = cust_records[0]['sys_id']
            state['cnx_number'] = cust_records[0].get('u_customer_id') or cust_records[0].get('u_number')

        return (user_exists and cust_exists), f"sys_user ID: {state['user1_id']}, Customer ID: {state['cust1_id']}"
    return False, f"HTTP {r.status_code}: {data}"

# ----------------------------------------------------
# TEST 002: Duplicate Registration
# ----------------------------------------------------
def t002():
    payload = {
        "name": cust1_name,
        "email": cust1_email,
        "mobile": cust1_mobile,
        "password": cust1_pass
    }
    r = requests.post(f"{API_BASE}/register", headers=headers, json=payload, timeout=15)
    data = r.json().get('result', r.json())
    if r.status_code == 400 and 'already exists' in data.get('error', '').lower():
        return True, f"Duplicate correctly rejected: {data.get('error')}"
    return False, f"Expected 400 rejection, got {r.status_code}: {data}"

# ----------------------------------------------------
# TEST 003: Customer Login
# ----------------------------------------------------
def t003():
    payload = {
        "email": cust1_email,
        "password": cust1_pass
    }
    r = requests.post(f"{API_BASE}/login", headers=headers, json=payload, timeout=15)
    data = r.json().get('result', r.json())
    if r.status_code == 200 and data.get('success'):
        return True, f"Authenticated successfully as: {data['user']['name']} ({data['user']['email']})"
    return False, f"Login failed: {data}"

# ----------------------------------------------------
# TEST 004: Dashboard Data
# ----------------------------------------------------
def t004():
    r = requests.get(f"{API_BASE}/cases?user_id={state['user1_id']}", headers=headers, timeout=15)
    data = r.json().get('result', r.json())
    if r.status_code == 200 and data.get('success'):
        stats = data.get('stats', {})
        total = stats.get('total', -1)
        active = stats.get('active', -1)
        resolved = stats.get('resolved', -1)
        is_zero = (total == 0 and active == 0 and resolved == 0)
        return is_zero, f"Dashboard Stats verified: Total={total}, Active={active}, Resolved={resolved}"
    return False, f"Failed fetching stats: {data}"

# ----------------------------------------------------
# TEST 005: Fraud Report
# ----------------------------------------------------
def t005():
    payload = {
        "user_id": state['user1_id'],
        "customer_id": state.get('customer1_sys_id', ''),
        "type": "Payment Fraud",
        "description": "Demo unauthorized payment reported for testing. 450,000 INR debited via fake UPI link.",
        "incident_date": "2026-10-02",
        "incident_time": "13:30",
        "severity": "High",
        "digital_platform": "DemoBank Mobile App",
        "location": "Mumbai",
        "area": "Andheri East",
        "pincode": "400069",
        "exposure": "450000",
        "evidence_type": "Image",
        "evidence_description": "Screenshot of deceptive UPI notification",
        "attachment_name": "fake_payment_alert.png"
    }
    r = requests.post(f"{API_BASE}/cases", headers=headers, json=payload, timeout=20)
    data = r.json().get('result', r.json())
    if r.status_code == 201 and data.get('success'):
        state['case1_sys_id'] = data['case_id']
        state['case1_number'] = data['number']
        return True, f"Fraud case created: {data['number']} (sys_id: {data['case_id']})"
    return False, f"Creation failed: {data}"

# ----------------------------------------------------
# TEST 006: Case Number
# ----------------------------------------------------
def t006():
    r = requests.get(f"{url}/api/now/table/u_x_fnx_case/{state['case1_sys_id']}", auth=admin_auth, headers=headers)
    rec = r.json().get('result', {})
    num = rec.get('number', '')
    if num.startswith('FNX'):
        return True, f"ServiceNow Number Maintenance verified: {num}"
    return False, f"Unexpected number: {num}"

# ----------------------------------------------------
# TEST 007: Evidence
# ----------------------------------------------------
def t007():
    r = requests.get(f"{url}/api/now/table/u_x_fnx_evidence?sysparm_query=u_case={state['case1_sys_id']}", auth=admin_auth, headers=headers)
    records = r.json().get('result', [])
    if len(records) > 0:
        state['ev1_sys_id'] = records[0]['sys_id']
        state['ev1_number'] = records[0].get('u_number') or records[0].get('sys_id')
        return True, f"Evidence record created: ID={state['ev1_number']}, Type={records[0].get('u_evidence_type')}"
    return False, "No evidence record found linked to case."

# ----------------------------------------------------
# TEST 008: Custody
# ----------------------------------------------------
def t008():
    r = requests.get(f"{url}/api/now/table/u_x_fnx_custody_log?sysparm_query=u_evidence={state['ev1_sys_id']}", auth=admin_auth, headers=headers)
    records = r.json().get('result', [])
    if len(records) > 0:
        return True, f"Custody log verified: Action={records[0].get('u_action')}, Performed By={records[0].get('u_performed_by')}"
    return False, "No custody log found for evidence."

# ----------------------------------------------------
# TEST 009: Audit
# ----------------------------------------------------
def t009():
    r = requests.get(f"{url}/api/now/table/u_x_fnx_audit?sysparm_query=u_case={state['case1_sys_id']}", auth=admin_auth, headers=headers)
    records = r.json().get('result', [])
    if len(records) > 0:
        return True, f"Audit log verified: Action={records[0].get('u_action')}, Details={records[0].get('u_details')}"
    return False, "No audit log found for case."

# ----------------------------------------------------
# TEST 010: Notification
# ----------------------------------------------------
def t010():
    r = requests.get(f"{url}/api/now/table/sysevent_email_action?sysparm_query=name=FNX - Case Submitted", auth=admin_auth, headers=headers)
    records = r.json().get('result', [])
    if len(records) > 0 and records[0].get('active') == 'true':
        return True, f"Case submission notification active on u_x_fnx_case: {records[0].get('name')}"
    return False, "Notification not found or inactive."

# ----------------------------------------------------
# TEST 011: Case Tracking
# ----------------------------------------------------
def t011():
    r = requests.get(f"{API_BASE}/cases?user_id={state['user1_id']}", headers=headers, timeout=15)
    data = r.json().get('result', r.json())
    cases = data.get('cases', [])
    found = any(c['sys_id'] == state['case1_sys_id'] for c in cases)
    if found:
        return True, f"Customer 1 successfully retrieved their case {state['case1_number']}"
    return False, f"Case not listed in user cases: {cases}"

# ----------------------------------------------------
# TEST 012: Security (Customer 2 cannot see Customer 1's case)
# ----------------------------------------------------
def t012():
    # Register Customer 2
    payload2 = {
        "name": cust2_name,
        "email": cust2_email,
        "mobile": cust2_mobile,
        "password": cust2_pass
    }
    r_reg2 = requests.post(f"{API_BASE}/register", headers=headers, json=payload2, timeout=15)
    data2 = r_reg2.json().get('result', r_reg2.json())
    state['user2_id'] = data2['user_id']
    
    # Query cases for Customer 2
    r_cases2 = requests.get(f"{API_BASE}/cases?user_id={state['user2_id']}", headers=headers, timeout=15)
    cases2 = r_cases2.json().get('result', r_cases2.json()).get('cases', [])
    
    # Ensure Customer 1's case is NOT present
    has_cust1_case = any(c['sys_id'] == state['case1_sys_id'] for c in cases2)
    if not has_cust1_case:
        return True, f"Security isolation verified: Customer 2 sees {len(cases2)} cases (Customer 1's case is strictly hidden)"
    return False, "Security failure: Customer 2 saw Customer 1's case!"

# ----------------------------------------------------
# TEST 013: Persistence
# ----------------------------------------------------
def t013():
    # Simulate logout and re-login
    payload = {"email": cust1_email, "password": cust1_pass}
    r = requests.post(f"{API_BASE}/login", headers=headers, json=payload, timeout=15)
    if r.status_code == 200:
        # Re-fetch cases
        r_cases = requests.get(f"{API_BASE}/cases?user_id={state['user1_id']}", headers=headers, timeout=15)
        cases = r_cases.json().get('result', r_cases.json()).get('cases', [])
        found = any(c['sys_id'] == state['case1_sys_id'] for c in cases)
        if found:
            return True, f"Persistence verified: Case {state['case1_number']} persisted across logout/relogin"
    return False, "Case did not persist across sessions"

# ----------------------------------------------------
# TEST 014: Direct Record Access ACL
# ----------------------------------------------------
def t014():
    # Test ACL directly: Fetch Customer 1's case using non-admin or unauthenticated
    r_no_auth = requests.get(f"{url}/api/now/table/u_x_fnx_case/{state['case1_sys_id']}")
    if r_no_auth.status_code in [401, 403]:
        return True, f"Direct unauthenticated access denied with HTTP {r_no_auth.status_code}"
    return False, f"Expected 401/403, got HTTP {r_no_auth.status_code}"

# ----------------------------------------------------
# TEST 015: Evidence Security
# ----------------------------------------------------
def t015():
    # Customer 2 should not see Customer 1's evidence
    r_no_auth_ev = requests.get(f"{url}/api/now/table/u_x_fnx_evidence/{state['ev1_sys_id']}")
    if r_no_auth_ev.status_code in [401, 403]:
        return True, f"Direct evidence access denied with HTTP {r_no_auth_ev.status_code}"
    return False, f"Expected 401/403, got HTTP {r_no_auth_ev.status_code}"

# EXECUTE ALL TESTS
tests = [
    ("TEST 001", "Customer Registration", t001),
    ("TEST 002", "Duplicate Registration", t002),
    ("TEST 003", "Customer Login", t003),
    ("TEST 004", "Dashboard Data", t004),
    ("TEST 005", "Fraud Report", t005),
    ("TEST 006", "Case Number", t006),
    ("TEST 007", "Evidence", t007),
    ("TEST 008", "Custody", t008),
    ("TEST 009", "Audit", t009),
    ("TEST 010", "Notification", t010),
    ("TEST 011", "Case Tracking", t011),
    ("TEST 012", "Security (Isolation between customers)", t012),
    ("TEST 013", "Persistence", t013),
    ("TEST 014", "Direct Record Access ACL", t014),
    ("TEST 015", "Evidence Security ACL", t015),
]

passed_count = 0
for tid, tname, tfn in tests:
    if run_test(tid, tname, tfn):
        passed_count += 1

print("\n" + "="*60)
print(f"TEST EXECUTION SUMMARY: {passed_count}/{len(tests)} TESTS PASSED")
print("="*60)
with open("test_summary.json", "w") as f:
    json.dump(test_results, f, indent=2)
