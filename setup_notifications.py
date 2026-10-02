import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def ensure_notification(name: str, collection: str, action_insert: bool, action_update: bool, subject: str, message_html: str, recipient_fields: str, condition: str = ""):
    r_chk = requests.get(f"{url}/api/now/table/sysevent_email_action?sysparm_query=name={name}", auth=auth, headers=headers)
    existing = r_chk.json().get('result', [])
    payload = {
        "name": name,
        "collection": collection,
        "action_insert": "true" if action_insert else "false",
        "action_update": "true" if action_update else "false",
        "subject": subject,
        "message_html": message_html,
        "recipient_fields": recipient_fields,
        "active": "true",
        "generation_type": "engine"
    }
    if condition:
        payload["condition"] = condition

    if existing:
        n_id = existing[0]['sys_id']
        requests.patch(f"{url}/api/now/table/sysevent_email_action/{n_id}", auth=auth, headers=headers, json=payload)
        print(f"Updated notification: {name}")
    else:
        requests.post(f"{url}/api/now/table/sysevent_email_action", auth=auth, headers=headers, json=payload)
        print(f"Created notification: {name}")

print("--- Registering Notifications ---")
n1_html = "<p>Dear Customer,</p><p>Your fraud report has been received.</p><p><strong>Case ID:</strong> ${number}<br><strong>Current Status:</strong> ${u_status}</p><p>Our investigation team has been notified. You can track real-time progress on your portal.</p>"
ensure_notification("FNX - Case Submitted", "u_x_fnx_case", True, False, "FRAUDNEXUS: Your fraud report ${number} has been received", n1_html, "u_reporter")

n2_html = "<p>Dear Customer,</p><p>There is an update on your fraud investigation.</p><p><strong>Case ID:</strong> ${number}<br><strong>New Status:</strong> ${u_status}<br><strong>Investigation Stage:</strong> ${u_stage}</p><p>Please log in to your portal to view full investigation notes.</p>"
ensure_notification("FNX - Case Status Updated", "u_x_fnx_case", False, True, "FRAUDNEXUS: Case ${number} Status Updated to ${u_status}", n2_html, "u_reporter", condition="u_statusVALCHANGES^EQ")

n3_html = "<p>Evidence record has been registered in the secure chain of custody log.</p><p><strong>Evidence ID:</strong> ${u_number}<br><strong>Type:</strong> ${u_evidence_type}</p>"
ensure_notification("FNX - Evidence Received", "u_x_fnx_evidence", True, False, "FRAUDNEXUS: Evidence ${u_number} received", n3_html, "u_uploaded_by")

print("All notifications configured!")
