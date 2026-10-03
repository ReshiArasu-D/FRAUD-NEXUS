import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('d:/KPMG/.env')
url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = (os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
endpoint = f"{url}/api/2229367/fnx_api/exec"

def run_script(js):
    r = requests.post(endpoint, auth=auth, json={"script": js})
    try:
        return r.json()
    except Exception as e:
        return {"error": str(e)}

seed_js = """
var result = { cases: [], tasks: [], evidence: [] };

// Handler map
var handlers = {};
var grUsers = new GlideRecord('sys_user');
grUsers.addQuery('email', 'IN', 'alex.morgan@fraudnexus.com,sophia.r@fraudnexus.com,james.d@fraudnexus.com,maria.k@fraudnexus.com,liam.t@fraudnexus.com,ava.p@fraudnexus.com');
grUsers.query();
while (grUsers.next()) {
    handlers[grUsers.getValue('email')] = grUsers.getUniqueValue();
}

// 1. Specific demo cases matching judge walkthrough & mockup
var demoCases = [
    {
        number: 'FNX-2026-001234',
        type: 'Unauthorized Transaction',
        severity: 'Critical',
        risk: 91,
        exposure: 250000,
        blocked: 50000,
        recovered: 0,
        status: 'New',
        stage: 'Initial Review',
        handler: null,
        desc: 'Unauthorized net-banking fund transfer of Rs 2,50,000 to an unknown beneficiary account via RTGS/IMPS at 02:15 AM.',
        incDate: '2026-01-12',
        platform: 'NetBanking / IMPS'
    },
    {
        number: 'FNX-2026-001233',
        type: 'Phishing',
        severity: 'High',
        risk: 78,
        exposure: 75000,
        blocked: 25000,
        recovered: 15000,
        status: 'Active',
        stage: 'Investigation',
        handler: handlers['sophia.r@fraudnexus.com'],
        desc: 'Customer received spoofed SMS purporting to be bank KYC update link, entered credentials and lost Rs 75,000.',
        incDate: '2026-01-11',
        platform: 'SMS / Mobile Web'
    },
    {
        number: 'FNX-2026-001229',
        type: 'Account Compromise',
        severity: 'High',
        risk: 72,
        exposure: 120000,
        blocked: 40000,
        recovered: 20000,
        status: 'Investigating',
        stage: 'Investigation',
        handler: handlers['james.d@fraudnexus.com'],
        desc: 'SIM swap fraud followed by corporate email account access and unauthorized beneficiary additions.',
        incDate: '2026-01-10',
        platform: 'Email / Corporate Portal'
    },
    {
        number: 'FNX-2026-001225',
        type: 'Identity Theft',
        severity: 'Medium',
        risk: 65,
        exposure: 45000,
        blocked: 10000,
        recovered: 35000,
        status: 'Active',
        stage: 'Investigation',
        handler: handlers['maria.k@fraudnexus.com'],
        desc: 'Fake credit card applied in victim name using forged Aadhaar and PAN card details.',
        incDate: '2026-01-09',
        platform: 'Fintech Credit App'
    },
    {
        number: 'FNX-2026-001220',
        type: 'Cyber Fraud',
        severity: 'Critical',
        risk: 88,
        exposure: 380000,
        blocked: 120000,
        recovered: 0,
        status: 'Escalated',
        stage: 'Investigation',
        handler: null,
        desc: '[ESCALATED] Ransomware extorting accounting firm with threat to publish financial transactions.',
        incDate: '2026-01-08',
        platform: 'Enterprise Network'
    },
    {
        number: 'FNX-2026-001218',
        type: 'Payment Fraud',
        severity: 'High',
        risk: 76,
        exposure: 95000,
        blocked: 30000,
        recovered: 10000,
        status: 'Active',
        stage: 'Investigation',
        handler: handlers['liam.t@fraudnexus.com'],
        desc: 'QR code scanning scam at merchant POS terminal directing funds to spoofed VPA.',
        incDate: '2026-01-07',
        platform: 'UPI / QR Code'
    },
    {
        number: 'FNX-2026-001215',
        type: 'Money Laundering',
        severity: 'Medium',
        risk: 58,
        exposure: 500000,
        blocked: 200000,
        recovered: 150000,
        status: 'Investigating',
        stage: 'Investigation',
        handler: handlers['ava.p@fraudnexus.com'],
        desc: 'Mule account ring channeling layering transactions across 14 newly opened current accounts.',
        incDate: '2026-01-06',
        platform: 'Core Banking API'
    },
    {
        number: 'FNX-2026-001210',
        type: 'Investment Scam',
        severity: 'High',
        risk: 80,
        exposure: 210000,
        blocked: 0,
        recovered: 0,
        status: 'New',
        stage: 'Initial Review',
        handler: null,
        desc: 'Fraudulent Telegram forex & crypto trading scheme promising 300% return in 48 hours.',
        incDate: '2026-01-05',
        platform: 'Telegram / Crypto Exchange'
    }
];

// Get or create sample customer
var grCust = new GlideRecord('u_x_fnx_customer');
grCust.query();
var custSysId = '';
if (grCust.next()) {
    custSysId = grCust.getUniqueValue();
}

for (var i = 0; i < demoCases.length; i++) {
    var dc = demoCases[i];
    var grC = new GlideRecord('u_x_fnx_case');
    grC.addQuery('number', dc.number);
    grC.query();
    var caseSysId = '';
    if (!grC.next()) {
        grC.initialize();
        grC.setValue('number', dc.number);
        grC.setValue('short_description', dc.type + ': ' + dc.number);
        grC.setValue('description', dc.desc);
        grC.setValue('u_type', dc.type);
        grC.setValue('u_severity', dc.severity);
        grC.setValue('u_risk_score', dc.risk);
        grC.setValue('u_exposure', dc.exposure);
        grC.setValue('u_blocked_amount', dc.blocked);
        grC.setValue('u_recovered_amount', dc.recovered);
        grC.setValue('u_status', dc.status);
        grC.setValue('u_stage', dc.stage);
        grC.setValue('u_source', 'Portal');
        grC.setValue('u_incident_date', dc.incDate);
        grC.setValue('u_digital_platform', dc.platform);
        if (dc.handler) {
            grC.setValue('assigned_to', dc.handler);
            grC.setValue('u_assigned_handler', dc.handler);
        }
        if (custSysId) grC.setValue('u_customer', custSysId);
        caseSysId = grC.insert();
        result.cases.push({ created: dc.number, id: caseSysId });
    } else {
        caseSysId = grC.getUniqueValue();
        grC.setValue('short_description', dc.type + ': ' + dc.number);
        grC.setValue('description', dc.desc);
        grC.setValue('u_type', dc.type);
        grC.setValue('u_severity', dc.severity);
        grC.setValue('u_risk_score', dc.risk);
        grC.setValue('u_exposure', dc.exposure);
        grC.setValue('u_blocked_amount', dc.blocked);
        grC.setValue('u_recovered_amount', dc.recovered);
        grC.setValue('u_status', dc.status);
        grC.setValue('u_stage', dc.stage);
        grC.setValue('u_incident_date', dc.incDate);
        grC.setValue('u_digital_platform', dc.platform);
        if (dc.handler) {
            grC.setValue('assigned_to', dc.handler);
            grC.setValue('u_assigned_handler', dc.handler);
        }
        if (custSysId) grC.setValue('u_customer', custSysId);
        grC.update();
        result.cases.push({ updated: dc.number, id: caseSysId });
    }

    // Evidence for each case
    var grEv = new GlideRecord('u_x_fnx_evidence');
    grEv.addQuery('u_case', caseSysId);
    grEv.query();
    if (!grEv.next()) {
        grEv.initialize();
        grEv.setValue('u_case', caseSysId);
        grEv.setValue('u_evidence_type', dc.type === 'Phishing' ? 'Digital Screenshot' : 'Bank Statement');
        grEv.setValue('u_description', 'Customer uploaded primary proof artifact for ' + dc.type);
        grEv.setValue('u_source', 'Customer');
        grEv.setValue('u_sha256_hash', '8f4c2e6b7d1a9c3e5f0a2b4d6e8c1a3b5d7e9f1a2c4e6b8d0a2c4e6b8d0a2c4e');
        grEv.setValue('u_processing_status', 'Completed');
        grEv.setValue('u_verification_status', 'Verified');
        var evId = grEv.insert();
        result.evidence.push({ "case": dc.number, id: evId });
    }

    // Tasks for investigation
    var grT = new GlideRecord('u_x_fnx_task');
    grT.addQuery('u_case', caseSysId);
    grT.query();
    if (!grT.next()) {
        grT.initialize();
        grT.setValue('u_case', caseSysId);
        grT.setValue('short_description', 'Perform bank account freeze & obtain beneficiary KYC');
        grT.setValue('description', 'Issue section 91 notice to intermediary bank for account freezing.');
        grT.setValue('priority', dc.severity === 'Critical' ? 'Critical' : 'High');
        grT.setValue('state', dc.status === 'New' ? 'Open' : 'In Progress');
        if (dc.handler) grT.setValue('assigned_to', dc.handler);
        var tId = grT.insert();
        result.tasks.push({ "case": dc.number, id: tId });
    }

    // Initial audit entry
    var grAud = new GlideRecord('u_x_fnx_audit');
    grAud.addQuery('u_case', caseSysId);
    grAud.query();
    if (!grAud.next()) {
        grAud.initialize();
        grAud.setValue('u_case', caseSysId);
        grAud.setValue('u_record_type', 'Case');
        grAud.setValue('u_record_id', dc.number);
        grAud.setValue('u_action', 'Case Created');
        grAud.setValue('u_details', 'Fraud report filed with exposure ₹' + dc.exposure);
        grAud.setValue('u_timestamp', new GlideDateTime());
        grAud.insert();
    }
}

return JSON.stringify(result);
"""

res = run_script(seed_js)
print("Seed Result:", json.dumps(res, indent=2))
