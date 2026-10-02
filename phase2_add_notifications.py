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
        r = requests.patch(f"{url}/api/now/table/sysevent_email_action/{n_id}", auth=auth, headers=headers, json=payload)
        print(f"Updated notification: {name} (status {r.status_code})")
    else:
        r = requests.post(f"{url}/api/now/table/sysevent_email_action", auth=auth, headers=headers, json=payload)
        print(f"Created notification: {name} (status {r.status_code})")

print("--- Registering Phase 2 Native Notifications ---")

notifications = [
    {
        "name": "FNX - Case Assigned",
        "collection": "u_x_fnx_case",
        "insert": False,
        "update": True,
        "subject": "FRAUDNEXUS: Investigator Assigned to Case ${number}",
        "html": "<p>Dear Customer,</p><p>An investigator has been assigned to your fraud case.</p><p><strong>Case:</strong> ${number}<br><strong>Investigator:</strong> ${assigned_to}</p><p>Log in to your FRAUDNEXUS portal to monitor progress.</p>",
        "recipient": "u_reporter",
        "condition": "assigned_toVALCHANGES^assigned_toISNOTEMPTY^EQ"
    },
    {
        "name": "FNX - Evidence Requested",
        "collection": "u_x_fnx_case",
        "insert": False,
        "update": True,
        "subject": "FRAUDNEXUS: Additional Evidence Requested for Case ${number}",
        "html": "<p>Dear Customer,</p><p>Our investigation team requires additional documentation or evidence for case <strong>${number}</strong>.</p><p>Please log in to FRAUDNEXUS and use the Evidence upload feature to attach supporting records.</p>",
        "recipient": "u_reporter",
        "condition": "u_status=Evidence Required^EQ"
    },
    {
        "name": "FNX - Case Escalated",
        "collection": "u_x_fnx_case",
        "insert": False,
        "update": True,
        "subject": "FRAUDNEXUS: Case ${number} Escalated for Priority Investigation",
        "html": "<p>Dear Customer,</p><p>Your fraud case <strong>${number}</strong> has been escalated for high-priority review and regulatory assessment.</p><p>You will receive further updates as forensic analysis progresses.</p>",
        "recipient": "u_reporter",
        "condition": "u_status=Escalated^EQ"
    },
    {
        "name": "FNX - Approval Update",
        "collection": "u_x_fnx_case",
        "insert": False,
        "update": True,
        "subject": "FRAUDNEXUS: Approval Status Update on Case ${number}",
        "html": "<p>Dear Customer,</p><p>An approval decision has been recorded for fraud case <strong>${number}</strong>.</p><p><strong>Approval Status:</strong> ${approval}</p>",
        "recipient": "u_reporter",
        "condition": "approvalVALCHANGES^EQ"
    },
    {
        "name": "FNX - Compliance Update",
        "collection": "u_x_fnx_case",
        "insert": False,
        "update": True,
        "subject": "FRAUDNEXUS: Compliance Review Notification for Case ${number}",
        "html": "<p>Dear Customer,</p><p>Your case <strong>${number}</strong> has entered the formal Compliance and Regulatory Review stage.</p>",
        "recipient": "u_reporter",
        "condition": "u_stage=Compliance Review^EQ"
    },
    {
        "name": "FNX - Case Resolved",
        "collection": "u_x_fnx_case",
        "insert": False,
        "update": True,
        "subject": "FRAUDNEXUS: Case ${number} Has Been Resolved",
        "html": "<p>Dear Customer,</p><p>We are pleased to inform you that investigation for case <strong>${number}</strong> has been completed and marked <strong>Resolved</strong>.</p><p>Resolution summary and findings are now available in your portal.</p>",
        "recipient": "u_reporter",
        "condition": "u_status=Resolved^EQ"
    },
    {
        "name": "FNX - Case Closed",
        "collection": "u_x_fnx_case",
        "insert": False,
        "update": True,
        "subject": "FRAUDNEXUS: Case ${number} Closed",
        "html": "<p>Dear Customer,</p><p>Case <strong>${number}</strong> is now formally closed.</p><p>Thank you for using FRAUDNEXUS Financial & Cyber Fraud Investigation Hub.</p>",
        "recipient": "u_reporter",
        "condition": "u_status=Closed^EQ"
    }
]

for n in notifications:
    ensure_notification(
        n["name"],
        n["collection"],
        n["insert"],
        n["update"],
        n["subject"],
        n["html"],
        n["recipient"],
        n.get("condition", "")
    )

print("--- Phase 2 Notifications Completed Successfully ---")
