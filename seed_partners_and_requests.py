"""
Seed synthetic demo partners and initial partner requests for FRAUDNEXUS.
All partners are clearly labelled as SIMULATED DEMO PARTNER.
"""
import requests
import os
import json
import time
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def run_seed():
    print("=" * 60)
    print("SEEDING PARTNERS & REQUESTS")
    print("=" * 60)

    # 1. Fetch some existing cases to link requests to
    r_cases = requests.get(
        f"{url}/api/now/table/u_x_fnx_case?sysparm_limit=10&sysparm_fields=sys_id,number,task_effective_number,short_description",
        auth=auth, headers=headers
    )
    cases = r_cases.json().get('result', [])
    case_ids = [c['sys_id'] for c in cases]
    print(f"Found {len(cases)} cases to link requests with.")

    # 2. Define synthetic demo partners
    demo_partners = [
        {
            "u_partner_number": "PRT-001001",
            "u_name": "Partner Bank A",
            "u_category": "Banks / Financial Institutions",
            "u_organization": "National Banking Alliance (Simulated)",
            "u_description": "Simulated Tier-1 retail & commercial banking partner for inter-bank transaction tracing, account freeze requests, and recipient verification.",
            "u_contact_person": "Vikram Seth (Simulated Liaison)",
            "u_contact_email": "partner-bank-a@demo.fraudnexus.org",
            "u_contact_phone": "+91 (0) 44 2810 5501",
            "u_status": "Active",
            "u_integration_type": "Simulated API",
            "u_endpoint_reference": "https://api.sim.fraudnexus.org/v1/bank-a/tracing",
            "u_sla": "4 Hours",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. High response rate during standard banking windows."
        },
        {
            "u_partner_number": "PRT-001002",
            "u_name": "Partner Bank B",
            "u_category": "Banks / Financial Institutions",
            "u_organization": "Apex Cooperative Banking Group (Simulated)",
            "u_description": "Cooperative banking node covering regional rural and semi-urban banking networks. Useful for secondary money mule account identification.",
            "u_contact_person": "Priya Ramanathan (Simulated Officer)",
            "u_contact_email": "coop-liaison@demo.fraudnexus.org",
            "u_contact_phone": "+91 (0) 44 2810 5502",
            "u_status": "Active",
            "u_integration_type": "REST API",
            "u_endpoint_reference": "https://api.sim.fraudnexus.org/v1/bank-b/records",
            "u_sla": "24 Hours",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. 24-hour turnaround SLA for official police reports."
        },
        {
            "u_partner_number": "PRT-001003",
            "u_name": "Payment Provider A",
            "u_category": "Payment Service Providers",
            "u_organization": "FastPay Digital Network (Simulated)",
            "u_description": "Unified payments interface and digital wallet network provider. Supports fast payment recall and QR merchant trace.",
            "u_contact_person": "Rahul Sen (Simulated Gateway Admin)",
            "u_contact_email": "ops@fastpay-sim.demo",
            "u_contact_phone": "+91 (0) 80 4120 7711",
            "u_status": "Active",
            "u_integration_type": "Simulated API",
            "u_endpoint_reference": "https://api.sim.fraudnexus.org/v1/fastpay/recall",
            "u_sla": "2 Hours",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. Immediate automated trace acknowledgment enabled."
        },
        {
            "u_partner_number": "PRT-001004",
            "u_name": "Cybersecurity Partner A",
            "u_category": "Cybersecurity / SOC Partners",
            "u_organization": "Sentinel Cyber Defense Labs (Simulated)",
            "u_description": "Specialized in malicious APK analysis, phishing domain takedown coordination, and compromised credential feed ingestion.",
            "u_contact_person": "Elena Rostova (Simulated Threat Lead)",
            "u_contact_email": "soc-takedown@sentinel-sim.demo",
            "u_contact_phone": "+1 415 555 0192",
            "u_status": "Active",
            "u_integration_type": "Webhook",
            "u_endpoint_reference": "https://hooks.sim.fraudnexus.org/sentinel/ioc",
            "u_sla": "1 Hour",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. Automated malicious domain quarantine workflow."
        },
        {
            "u_partner_number": "PRT-001005",
            "u_name": "Threat Intelligence Provider A",
            "u_category": "Threat Intelligence Providers",
            "u_organization": "DarkNet Sentinel Intelligence (Simulated)",
            "u_description": "Dark web telegram channel monitoring, compromised card marketplace dumps, and cyber extortion syndicate tracking.",
            "u_contact_person": "Marcus Vance (Simulated Intel Analyst)",
            "u_contact_email": "intel-feed@darknet-sim.demo",
            "u_contact_phone": "+44 20 7946 0991",
            "u_status": "Active",
            "u_integration_type": "REST API",
            "u_endpoint_reference": "https://api.sim.fraudnexus.org/v1/darkintel/feed",
            "u_sla": "6 Hours",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. Provides syndicate profile hashes and IOC correlation."
        },
        {
            "u_partner_number": "PRT-001006",
            "u_name": "AML Partner A",
            "u_category": "AML / Financial Crime Partners",
            "u_organization": "Global AML Watchdog Systems (Simulated)",
            "u_description": "Anti-Money Laundering transaction monitoring, sanctions list cross-checking, and PEP (Politically Exposed Persons) screening.",
            "u_contact_person": "Ananya Roy (Simulated AML Director)",
            "u_contact_email": "compliance@aml-watchdog-sim.demo",
            "u_contact_phone": "+91 (0) 22 6670 4422",
            "u_status": "Active",
            "u_integration_type": "Simulated API",
            "u_endpoint_reference": "https://api.sim.fraudnexus.org/v1/aml/screen",
            "u_sla": "12 Hours",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. Real-time screening against global watchlist snapshots."
        },
        {
            "u_partner_number": "PRT-001007",
            "u_name": "KYC Provider A",
            "u_category": "KYC / Identity Verification Partners",
            "u_organization": "VeriTrust Identity Services (Simulated)",
            "u_description": "Biometric face matching, government document OCR validation, and synthetic identity fraud detection.",
            "u_contact_person": "Siddharth Rao (Simulated Verification Head)",
            "u_contact_email": "support@veritrust-sim.demo",
            "u_contact_phone": "+91 (0) 80 2341 8890",
            "u_status": "Active",
            "u_integration_type": "REST API",
            "u_endpoint_reference": "https://api.sim.fraudnexus.org/v1/kyc/verify",
            "u_sla": "30 Mins",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. Near instant biometric and document score verification."
        },
        {
            "u_partner_number": "PRT-001008",
            "u_name": "Regulatory Partner A",
            "u_category": "Regulatory / Compliance Authorities",
            "u_organization": "Central Cyber Crime Regulatory Cell (Simulated)",
            "u_description": "Regulatory portal for statutory reporting of cyber incidents exceeding threshold exposure values.",
            "u_contact_person": "Dr. K. Swaminathan (Simulated Joint Sec)",
            "u_contact_email": "nodal-desk@regulator-sim.demo",
            "u_contact_phone": "+91 (0) 11 2309 3344",
            "u_status": "Active",
            "u_integration_type": "Manual",
            "u_endpoint_reference": "https://portal.regulator-sim.demo/statutory-filings",
            "u_sla": "48 Hours",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. Requires verified case summary before statutory acknowledgement."
        },
        {
            "u_partner_number": "PRT-001009",
            "u_name": "Investigation Authority A",
            "u_category": "Law Enforcement / Investigation Authorities",
            "u_organization": "State Cyber Crime Police Wing (Simulated)",
            "u_description": "Law enforcement liaison for Section 91 CrPC notices, electronic evidence seizure orders, and judicial warrant dispatch.",
            "u_contact_person": "Inspector R. Balaji (Simulated Cyber Inspector)",
            "u_contact_email": "cyber-ps@le-liaison-sim.demo",
            "u_contact_phone": "+91 (0) 44 2844 7788",
            "u_status": "Active",
            "u_integration_type": "Email",
            "u_endpoint_reference": "mailto:investigations@le-liaison-sim.demo",
            "u_sla": "24 Hours",
            "u_demo_flag": True,
            "u_active": True,
            "u_notes": "SIMULATED DEMO PARTNER. Submits formal evidence preservation notices."
        },
        {
            "u_partner_number": "PRT-001010",
            "u_name": "Legacy Merchant Gateway",
            "u_category": "Payment Gateways / Payment Platforms",
            "u_organization": "TransactPro Legacy Systems (Simulated)",
            "u_description": "Archived credit card settlement gateway undergoing system migration. Temporarily inactive.",
            "u_contact_person": "Arun Kumar (Simulated Maintainer)",
            "u_contact_email": "legacy-ops@transactpro-sim.demo",
            "u_contact_phone": "+91 (0) 22 4001 9911",
            "u_status": "Inactive",
            "u_integration_type": "Import",
            "u_endpoint_reference": "sftp://sftp.sim.fraudnexus.org/incoming",
            "u_sla": "72 Hours",
            "u_demo_flag": True,
            "u_active": False,
            "u_notes": "SIMULATED DEMO PARTNER. Inactive partner for testing reactivation and filtering workflows."
        }
    ]

    partner_map = {} # name -> sys_id
    for p in demo_partners:
        # Check if already exists
        r_chk = requests.get(
            f"{url}/api/now/table/u_x_fnx_partner?sysparm_query=u_name={p['u_name']}",
            auth=auth, headers=headers
        )
        existing = r_chk.json().get('result', [])
        if existing:
            p_id = existing[0]['sys_id']
            partner_map[p['u_name']] = p_id
            print(f"[EXISTS] Partner: {p['u_name']} ({p_id})")
        else:
            r_ins = requests.post(
                f"{url}/api/now/table/u_x_fnx_partner",
                auth=auth, headers=headers, json=p
            )
            if r_ins.status_code in [200, 201]:
                p_id = r_ins.json().get('result', {}).get('sys_id')
                partner_map[p['u_name']] = p_id
                print(f"[INSERTED] Partner: {p['u_name']} ({p_id})")
            else:
                print(f"[ERROR] Inserting partner {p['u_name']}: {r_ins.status_code} - {r_ins.text[:100]}")

    # 3. Seed demo partner requests
    demo_requests = [
        {
            "u_request_number": "PRTREQ-001001",
            "u_partner_name": "Partner Bank A",
            "u_case_idx": 0,
            "u_request_type": "Request Transaction Information",
            "u_requested_by": "Alex Morgan",
            "u_priority": "Critical",
            "u_description": "Request immediate transaction verification and beneficiary account freeze for fraudulent IMPS/UPI transfer of INR 75,000.",
            "u_reference": "TXN-2026-992144 / UTR-DEMO-001",
            "u_status": "Response Received",
            "u_response": "SIMULATED INTEGRATION RESPONSE: Beneficiary account [HDFC-****4412] successfully flagged. Freeze order applied to INR 25,000 remaining balance. Originating IP 198.51.100.44 confirmed from known VPN exit node.",
            "u_resolution_notes": "Partial funds secured. Forwarded to Case Investigator Alex Morgan.",
            "u_demo_request": True
        },
        {
            "u_request_number": "PRTREQ-001002",
            "u_partner_name": "Payment Provider A",
            "u_case_idx": 1,
            "u_request_type": "Request Payment Trace",
            "u_requested_by": "Alex Morgan",
            "u_priority": "High",
            "u_description": "Trace multi-hop wallet transfers across secondary merchant accounts linked to fraudulent QR code campaign.",
            "u_reference": "QR-MERCH-8812 / UPI-TRACE-8841",
            "u_status": "In Progress",
            "u_response": "SIMULATED INTEGRATION IN-FLIGHT: Wallet hops 1 and 2 traced. Awaiting final merchant settlement clearing house logs.",
            "u_resolution_notes": "",
            "u_demo_request": True
        },
        {
            "u_request_number": "PRTREQ-001003",
            "u_partner_name": "Cybersecurity Partner A",
            "u_case_idx": 2,
            "u_request_type": "Request Threat Intelligence",
            "u_requested_by": "Sophia Reynolds",
            "u_priority": "Critical",
            "u_description": "Analyze malicious APK package 'Electricity_Bill_Update.apk' captured from victim's mobile device for C2 command endpoints.",
            "u_reference": "HASH: 8f4a21e69b91c49b01aaef984532e18b",
            "u_status": "Completed",
            "u_response": "SIMULATED MALWARE ANALYSIS: APK identified as 'HydraDropper.v4'. C2 infrastructure located at 185.220.101.5. C2 server neutralized via upstream registrar takedown request.",
            "u_resolution_notes": "C2 neutralized. Indicators of compromise added to FRAUDNEXUS Intelligence Workspace.",
            "u_demo_request": True
        },
        {
            "u_request_number": "PRTREQ-001004",
            "u_partner_name": "KYC Provider A",
            "u_case_idx": 0,
            "u_request_type": "Request KYC Verification",
            "u_requested_by": "James Davis",
            "u_priority": "Medium",
            "u_description": "Verify identity credentials submitted for suspect account created 2 hours prior to fraud execution.",
            "u_reference": "ID-PAN-ABCDE1234F / AADHAAR-****8819",
            "u_status": "Awaiting Response",
            "u_response": "",
            "u_resolution_notes": "",
            "u_demo_request": True
        },
        {
            "u_request_number": "PRTREQ-001005",
            "u_partner_name": "Partner Bank B",
            "u_case_idx": 1,
            "u_request_type": "Request Account Information",
            "u_requested_by": "Alex Morgan",
            "u_priority": "High",
            "u_description": "Statutory request for KYC documents and 60-day ledger history for suspect account involved in money mule ring.",
            "u_reference": "ACC-66019924-MULE",
            "u_status": "Overdue",
            "u_response": "",
            "u_resolution_notes": "SLA breached (24 Hours). Escalation reminder dispatched to Bank B liaison officer.",
            "u_demo_request": True
        }
    ]

    for req in demo_requests:
        r_num = req["u_request_number"]
        r_chk = requests.get(
            f"{url}/api/now/table/u_x_fnx_partner_request?sysparm_query=u_request_number={r_num}",
            auth=auth, headers=headers
        )
        if r_chk.json().get('result', []):
            print(f"[EXISTS] Partner Request: {r_num}")
            continue

        p_name = req.pop("u_partner_name")
        p_id = partner_map.get(p_name, "")
        case_idx = req.pop("u_case_idx")
        c_id = case_ids[case_idx] if case_idx < len(case_ids) else ""

        req["u_partner"] = p_id
        req["u_case"] = c_id

        r_ins = requests.post(
            f"{url}/api/now/table/u_x_fnx_partner_request",
            auth=auth, headers=headers, json=req
        )
        if r_ins.status_code in [200, 201]:
            print(f"[INSERTED] Partner Request: {r_num} for {p_name}")
        else:
            print(f"[ERROR] Inserting request {r_num}: {r_ins.status_code} - {r_ins.text[:100]}")

    print("\n--- Seeding Complete ---")

if __name__ == "__main__":
    run_seed()
