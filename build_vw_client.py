import os, sys

sys.stdout.reconfigure(encoding='utf-8')

js_content = """/* ============================================================
   FRAUDNEXUS — VERIFICATION WORKSPACE CLIENT CONTROLLER EXTENSION
   Sections C–AB Implementation
   ============================================================ */

    // 1. Initialize Verification Workspace State
    c.investigationTab = 'overview';
    c.verificationQueueFilter = 'all';
    c.reportSubTab = 'admin';
    c.timelineFilter = 'all';
    c.showMoreActions = false;
    c.showGenAIModal = false;
    c.showPartnerReqModal = false;
    c.showAlertCustomerModal = false;
    c.showAlertWorkerModal = false;
    c.selectedGenAIMode = 'journey';
    c.currentDateStr = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });

    // 2. Default Rich Demo Case Structure (Section 35 Scenario)
    c.setupDefaultInvestigationCase = function() {
        return {
            sys_id: 'case_fnx_2026_00847',
            number: 'FNX-2026-00847',
            type: 'Phishing / Financial Fraud',
            incident_type: 'Phishing / Financial Fraud',
            severity: 'Critical',
            priority: 'P1 - Critical',
            status: 'In Progress',
            stage: 'Evidence Verification',
            risk_score: 94,
            exposure: 85000,
            verified_exposure: 85000,
            blocked_amount: 35000,
            recovered_amount: 0,
            sla: '3h 45m remaining',
            created_on: '2026-10-02 14:22 IST',
            updated_on: 'Just now',
            handler: 'Alex Morgan',
            incident_date: '2026-10-02 14:15 IST',
            platform: 'UPI / Mobile NetBanking',
            description: 'Customer received an urgent SMS masquerading as HDFC Bank KYC update alert. The link redirected to a spoofed login portal capturing credentials. An unauthorized UPI transaction of INR 85,000 was executed to an unknown beneficiary merchant within 5 minutes.',
            customer: {
                customer_id: 'CUST-84920',
                name: 'Rajesh Sharma',
                email: 'rajesh.sharma@example.com',
                mobile: '+91 98401 23456',
                kyc_status: 'Verified',
                account_num: 'XXXX-XXXX-4819'
            },
            evidence: [
                {
                    id: 'EV-001',
                    title: 'Phishing SMS Screenshot',
                    icon: '📱',
                    type: 'Image / Screenshot',
                    source: 'Customer Mobile Upload',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:25',
                    classification: 'JOREN: SMS Smishing Indicator',
                    pipeline: 'JOREN Multimodal Vision OCR',
                    extracted_info: 'Sender VK-HDFCBK. Deceptive message claiming NetBanking deactivation in 24 hours. Bit.ly redirect url.',
                    entities: ['HDFC Bank Spoof', 'Urgent Call to Action', 'SMS Gateway VK-HDFCBK'],
                    sha256: 'a4b2c1d98e7f60321a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f',
                    status: 'Confirmed',
                    notes: 'Matches known banking smishing campaign reported to Cert-In.'
                },
                {
                    id: 'EV-002',
                    title: 'Malicious Harvesting URL Screenshot',
                    icon: '🌐',
                    type: 'Image / URL Capture',
                    source: 'Customer Browser Cache',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:28',
                    classification: 'JOREN: Fake Banking Credential Harvester',
                    pipeline: 'JOREN Web Threat Intelligence',
                    extracted_info: 'Domain: secure-bank-login-verify.com. Fake HDFC NetBanking logo, captured credentials & OTP field.',
                    url_ref: 'hxxps://secure-bank-login-verify.com/login',
                    entities: ['Credential Harvester', 'Domain Impersonation', 'Fake NetBanking UI'],
                    sha256: '9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e',
                    status: 'Confirmed',
                    notes: 'Domain registered 48 hours prior to attack on privacy registrar.'
                },
                {
                    id: 'EV-003',
                    title: 'Bank Transaction Statement PDF',
                    icon: '📄',
                    type: 'Document / Financial PDF',
                    source: 'Official Statement Download',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:32',
                    classification: 'JOREN: High-Value Debit Record',
                    pipeline: 'JOREN PDF Financial Extractor',
                    extracted_info: 'Debit of INR 85,000.00 via UPI on 2026-10-02 at 14:22:18 IST. Ref: UPI/2026/84920194819 to pay-fast-merchant@ybl.',
                    transaction_ref: 'UPI/2026/84920194819',
                    entities: ['UPI Protocol', 'Amount: INR 85,000', 'Beneficiary: pay-fast-merchant@ybl'],
                    sha256: '5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d',
                    status: 'Confirmed',
                    notes: 'Financial debit corroborated by Partner Bank A ledger.'
                },
                {
                    id: 'EV-004',
                    title: 'Bank Debit Confirmation Email',
                    icon: '✉️',
                    type: 'Email / EML Export',
                    source: 'Customer Mailbox',
                    submitter: 'Rajesh Sharma',
                    date: '2026-10-02 14:35',
                    classification: 'JOREN: Authentic Bank Transaction Alert',
                    pipeline: 'JOREN Email RFC-822 Parser',
                    extracted_info: 'Automated transaction confirmation from alerts@hdfcbank.net confirming immediate debit of INR 85,000.',
                    transaction_ref: 'UPI/2026/84920194819',
                    entities: ['Transaction Notification', 'Timestamp Corroboration'],
                    sha256: '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b',
                    status: 'Confirmed',
                    notes: 'Validates timing within 7 minutes of victim credential entry.'
                }
            ],
            findings: [
                {
                    id: 'FND-001',
                    title: 'Targeted SMS Smishing Campaign masquerading as HDFC Bank',
                    description: 'Deceptive SMS received from bulk spoofed route claiming urgent KYC deactivation ultimatum.',
                    supporting_evidence: ['EV-001'],
                    confidence: 98,
                    source: 'AI Generated',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:00',
                    notes: 'Matches signature of known syndicate smishing wave.'
                },
                {
                    id: 'FND-002',
                    title: 'Credential Harvesting Domain hosted on suspicious ASN',
                    description: 'The domain secure-bank-login-verify.com was spun up to capture NetBanking credentials and session OTPs.',
                    supporting_evidence: ['EV-002'],
                    confidence: 96,
                    source: 'AI Generated',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:05',
                    notes: 'Reported to national domain registrar for immediate takedown.'
                },
                {
                    id: 'FND-003',
                    title: 'Account Compromise via Unrecognized Foreign Tor IP',
                    description: 'Attacker accessed customer NetBanking from Tor exit node IP 185.220.101.5 within 4 minutes of harvest.',
                    supporting_evidence: ['EV-002', 'EV-003'],
                    confidence: 94,
                    source: 'AI Generated',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:10',
                    notes: 'Impossible travel anomaly confirmed by session telemetry.'
                },
                {
                    id: 'FND-004',
                    title: 'High-Velocity Unauthorized UPI Transaction to Flagged Mule',
                    description: 'Instant transfer of INR 85,000 sent to beneficiary pay-fast-merchant@ybl which has 4 prior fraud liens.',
                    supporting_evidence: ['EV-003', 'EV-004'],
                    confidence: 99,
                    source: 'Investigator Identified',
                    status: 'Confirmed',
                    reviewer: 'Alex Morgan',
                    reviewed_on: '2026-10-02 15:15',
                    notes: 'Corroborated by Partner Bank A response trace.'
                }
            ],
            cyber: {
                indicators: [
                    { type: 'Domain', value: 'secure-bank-login-verify.com', classification: 'Phishing Harvester', first_seen: '2026-09-30', reputation: 'Malicious', syndicate: 'Fake-Bank-Smish-2026' },
                    { type: 'IP', value: '185.220.101.5', classification: 'Tor Exit Node / Anonymizer', first_seen: '2026-08-14', reputation: 'Critical Threat', syndicate: 'Cluster-Tor-Node-5' },
                    { type: 'SMS Sender', value: 'VK-HDFCBK', classification: 'Spoofed Bank Sender ID', first_seen: '2026-10-02', reputation: 'Blocked', syndicate: 'Fake-Bank-Smish-2026' },
                    { type: 'UPI Mule', value: 'pay-fast-merchant@ybl', classification: 'Money Mule Account', first_seen: '2026-09-12', reputation: 'Flagged Lien', syndicate: 'Syndicate-Mule-Tier2' },
                    { type: 'User Agent', value: 'HeadlessChrome/124.0.0.0', classification: 'Automated Browser Bot', first_seen: '2026-10-02', reputation: 'High Risk', syndicate: 'Automated Exploitation' }
                ]
            },
            notes: [
                {
                    author: 'Alex Morgan',
                    role: 'Lead Investigator',
                    timestamp: '2026-10-02 14:40 IST',
                    text: 'Case assigned. Initial review of customer report completed. Verified victim KYC identity matches the remitter account. Proceeding with JOREN artifact classification.',
                    tags: ['Intake', 'Verification']
                },
                {
                    author: 'Alex Morgan',
                    role: 'Lead Investigator',
                    timestamp: '2026-10-02 15:20 IST',
                    text: 'Dispatched urgent inter-bank trace PR-001 to Partner Bank A requesting account lien on beneficiary pay-fast-merchant@ybl.',
                    tags: ['PartnerTrace', 'FundRecovery']
                },
                {
                    author: 'Alex Morgan',
                    role: 'Lead Investigator',
                    timestamp: '2026-10-02 15:50 IST',
                    text: 'Partner Bank A confirmed unauthorized transaction. ₹ 35,000 held at destination node. Risk score elevated to 94 (Critical). Preparing final resolution statement.',
                    tags: ['PartnerResponse', 'RiskUpdate']
                }
            ],
            partner_requests: [
                {
                    id: 'PR-001',
                    partner: 'Partner Bank A - SIMULATED DEMO PARTNER',
                    demo_flag: true,
                    request_type: 'Transaction Verification',
                    priority: 'P1 - Critical',
                    status: 'Response Received',
                    due_date: '2026-10-02 18:00 IST',
                    description: 'Transaction TXN-2026-84920194819 for INR 85,000 on 2026-10-02 at 14:22 requires verification of authorization status and immediate beneficiary account lien.',
                    response: {
                        received_on: '2026-10-02 15:45 IST',
                        verification_result: 'CONFIRMED UNAUTHORIZED / SUSPECTED MULE NODE',
                        details: 'Partner Bank A internal audit verifies the transaction was received at 14:22:19. Recipient account pay-fast-merchant@ybl showed sudden burst velocity inconsistent with historic profile. Full debit freeze enacted.',
                        beneficiary_bank: 'Yes Bank Cooperative Switch',
                        account_status: 'FROZEN / LIEN PLACED',
                        held_amount: 35000
                    },
                    ai_analysis: {
                        classification: 'Confirms Unauthorized Transaction & Laundering Node',
                        supporting_info: 'Partner response timestamp correlates with victim login alert within 18 seconds. Beneficiary account freeze holds INR 35,000 for potential clawback.',
                        contradictions: null,
                        suggested_finding_update: 'FND-004: Status verified as confirmed fraudulent money mule.',
                        suggested_risk_impact: 'Elevate Case Risk to 94/100 (Critical)'
                    },
                    analysis_accepted: true
                }
            ],
            related_cases: [
                {
                    number: 'FNX-2026-00792',
                    type: 'Phishing / Unauthorized UPI',
                    status: 'Resolved',
                    shared_indicators: ['secure-bank-login-verify.com', '185.220.101.5'],
                    similarity: 94,
                    pattern_desc: 'Identical phishing domain registrar and Tor exit node login IP.'
                },
                {
                    number: 'FNX-2026-00651',
                    type: 'Account Takeover',
                    status: 'Closed',
                    shared_indicators: ['VK-HDFCBK', 'pay-fast-merchant@ybl'],
                    similarity: 82,
                    pattern_desc: 'Shared SMS sender header and common money mule beneficiary.'
                }
            ],
            relationships: [
                { source: 'Rajesh Sharma', source_type: 'Customer', relationship: 'Victim Of', target: 'FNX-2026-00847', target_type: 'Case', confidence: 100, evidence_ref: 'EV-001', status: 'Confirmed' },
                { source: 'FNX-2026-00847', source_type: 'Case', relationship: 'Involves Domain', target: 'secure-bank-login-verify.com', target_type: 'Threat Infra', confidence: 98, evidence_ref: 'EV-002', status: 'Confirmed' },
                { source: 'secure-bank-login-verify.com', source_type: 'Threat Infra', relationship: 'Resolves To', target: '185.220.101.5', target_type: 'Tor IP', confidence: 96, evidence_ref: 'EV-002', status: 'Confirmed' },
                { source: '185.220.101.5', source_type: 'Tor IP', relationship: 'Executed Txn', target: 'UPI/2026/84920194819', target_type: 'Transaction', confidence: 95, evidence_ref: 'EV-003', status: 'Confirmed' },
                { source: 'UPI/2026/84920194819', source_type: 'Transaction', relationship: 'Credited To', target: 'pay-fast-merchant@ybl', target_type: 'Mule Account', confidence: 99, evidence_ref: 'EV-003', status: 'Confirmed' },
                { source: 'pay-fast-merchant@ybl', source_type: 'Mule Account', relationship: 'Settled Via', target: 'Partner Bank A', target_type: 'Partner Bank', confidence: 100, evidence_ref: 'PR-001', status: 'Confirmed' },
                { source: 'FNX-2026-00847', source_type: 'Case', relationship: 'Correlated With', target: 'FNX-2026-00792', target_type: 'Related Case', confidence: 94, evidence_ref: 'KnowledgeGraph', status: 'Confirmed' },
                { source: 'secure-bank-login-verify.com', source_type: 'Threat Infra', relationship: 'Attributed To', target: 'Fake-Bank-Smish-2026', target_type: 'Syndicate', confidence: 92, evidence_ref: 'ThreatIntel', status: 'Confirmed' }
            ],
            risk_factors: [
                { name: 'Smishing SMS Vector Confirmed', points: 25, evaluation: 'Spoofed bank sender ID with urgent threat of deactivation.' },
                { name: 'High-Value Immediate Fund Siphoning', points: 30, evaluation: 'Transfer of INR 85,000 within 5 minutes of credential harvest.' },
                { name: 'Anonymized Foreign IP Login (Tor)', points: 20, evaluation: 'Login originating from 185.220.101.5 (Germany Tor Node).' },
                { name: 'Verified Mule Beneficiary Account', points: 19, evaluation: 'Partner Bank A confirmed account has prior fraud reports.' }
            ],
            risk_history: [
                { stage: '1. Initial Intake', score: 55, reason: 'Customer reported fraud via mobile portal.', time: '14:22' },
                { stage: '2. Evidence Submitted', score: 68, reason: 'Ingested SMS, URL screenshot, and statement.', time: '14:35' },
                { stage: '3. Findings Confirmed', score: 78, reason: 'Investigator confirmed credential theft.', time: '15:15' },
                { stage: '4. Partner Bank Verified', score: 94, reason: 'Partner Bank A verified unauthorized debit.', time: '15:50' }
            ],
            tasks: [
                { number: 'TSK-001', short_description: 'Verify Customer KYC & Mobile Ownership', assigned_to: 'Alex Morgan', priority: 'High', due_date: '2026-10-02 16:00', state: 'Completed' },
                { number: 'TSK-002', short_description: 'Dispatch Partner Inter-bank Trace to Partner Bank A', assigned_to: 'Alex Morgan', priority: 'High', due_date: '2026-10-02 17:00', state: 'Completed' },
                { number: 'TSK-003', short_description: 'Initiate Zero-Liability Claim Reimbursement Advice', assigned_to: 'Alex Morgan', priority: 'High', due_date: '2026-10-02 18:00', state: 'Completed' }
            ],
            compliance: [
                { framework: 'RBI Master Direction - Digital Fraud', requirement: 'Reporting within 24 hours of confirmation', deadline: '2026-10-03 14:00', status: 'Compliant (Filed Form FMR-1)' },
                { framework: 'Cert-In Cyber Security Incident', requirement: 'Phishing domain notification to national CSIRT', deadline: '2026-10-03 12:00', status: 'Compliant (Advisory Issued)' },
                { framework: 'Customer Zero-Liability Protection', requirement: 'Lien advice & reimbursement authorization', deadline: '2026-10-04 17:00', status: 'Compliant (Advice Dispatched)' },
                { framework: 'PCI-DSS Data Minimization', requirement: 'Zero credential/PIN retention verification', deadline: 'Continuous', status: 'Compliant (No Credentials Stored)' },
                { framework: 'Digital Evidence Chain of Custody', requirement: 'SHA256 cryptographic immutability log', deadline: 'Continuous', status: 'Compliant (Unbroken Hashes)' }
            ],
            custody_log: [
                { timestamp: '2026-10-02 14:25:12', evidence_id: 'EV-001', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: 'a4b2c1d98e7f60321a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f' },
                { timestamp: '2026-10-02 14:28:44', evidence_id: 'EV-002', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: '9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e' },
                { timestamp: '2026-10-02 14:32:05', evidence_id: 'EV-003', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: '5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d' },
                { timestamp: '2026-10-02 14:35:19', evidence_id: 'EV-004', action: 'Upload & SHA256 Computed', custodian: 'Rajesh Sharma / JOREN Ingest', hash: '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b' },
                { timestamp: '2026-10-02 15:00:00', evidence_id: 'EV-ALL', action: 'Forensic Review & Validation', custodian: 'Alex Morgan (Senior Investigator)', hash: 'f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3' }
            ],
            timeline: [
                { time: '14:15 IST', actor: 'Rajesh Sharma', actor_type: 'HUMAN', action: 'Incident Incurred', desc: 'Customer clicked phishing link and lost INR 85,000.', record_id: 'EV-001' },
                { time: '14:22 IST', actor: 'Rajesh Sharma', actor_type: 'HUMAN', action: 'Case Submitted', desc: 'Fraud report submitted via FRAUDNEXUS customer portal.', record_id: 'FNX-2026-00847' },
                { time: '14:23 IST', actor: 'FNX Platform', actor_type: 'SYSTEM', action: 'Case Registered', desc: 'Case auto-registered, priority P1 assigned, SLA timer initialized.', record_id: 'FNX-2026-00847' },
                { time: '14:26 IST', actor: 'JOREN Pipeline', actor_type: 'AI SYSTEM', action: 'Evidence Ingestion', desc: 'JOREN multimodal vision model extracted text from phishing SMS.', record_id: 'EV-001' },
                { time: '14:30 IST', actor: 'JOREN Pipeline', actor_type: 'AI SYSTEM', action: 'Threat Classification', desc: 'Malicious domain identified as credential harvester.', record_id: 'EV-002' },
                { time: '14:35 IST', actor: 'FNX Platform', actor_type: 'SYSTEM', action: 'Investigator Assigned', desc: 'Assigned to Senior Investigator Alex Morgan.', record_id: 'USR-AM' },
                { time: '15:00 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Evidence Confirmed', desc: 'Investigator confirmed all 4 submitted artifacts.', record_id: 'EV-ALL' },
                { time: '15:15 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Findings Confirmed', desc: 'Investigator reviewed and confirmed 4 AI findings.', record_id: 'FND-ALL' },
                { time: '15:20 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Partner Request Submitted', desc: 'Dispatched inter-bank trace PR-001 to Partner Bank A.', record_id: 'PR-001' },
                { time: '15:45 IST', actor: 'Partner Bank A', actor_type: 'HUMAN', action: 'Partner Response Received', desc: 'Partner Bank A confirmed unauthorized transaction and froze mule node.', record_id: 'PR-001' },
                { time: '15:50 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Risk Elevated to Critical', desc: 'Risk elevated to 94/100 following partner verification.', record_id: 'RISK-94' },
                { time: '16:00 IST', actor: 'Generative AI', actor_type: 'AI SYSTEM', action: 'Synthesis Generated', desc: 'Synthesized Case Journey Summary for investigator review.', record_id: 'GENAI-01' },
                { time: '16:15 IST', actor: 'Marcus Vance', actor_type: 'HUMAN', action: 'Manager Approval Granted', desc: 'Fraud Operations Director approved zero-liability resolution.', record_id: 'APP-MV' },
                { time: '16:20 IST', actor: 'Alex Morgan', actor_type: 'HUMAN', action: 'Case Resolved', desc: 'Formal resolution recorded: Confirmed Fraud. Customer report dispatched.', record_id: 'FNX-2026-00847' }
            ],
            decision: {
                status: 'Resolved',
                outcome: 'Confirmed Fraud',
                reason: 'Investigation confirms credentials were harvested via smishing domain secure-bank-login-verify.com. The unauthorized debit of INR 85,000 on 2026-10-02 has been verified by Partner Bank A. A lien of INR 35,000 is active on the beneficiary node. Reversal advice initiated.',
                investigator: 'Alex Morgan',
                timestamp: '2026-10-02 16:20 IST'
            },
            manager_approved: true
        };
    };

    // 3. FNXCaseContextBuilder (Section 22 & O.1 Implementation)
    c.buildFNXCaseContext = function() {
        var cs = c.activeInvestigationCase;
        if (!cs) return {};

        // Sanitize and filter
        return {
            case_number: cs.number,
            incident_type: cs.incident_type || cs.type,
            severity: cs.severity,
            priority: cs.priority,
            current_status: cs.status,
            risk_score: cs.risk_score,
            risk_level: c.getRiskLabel(cs.risk_score),
            reported_exposure: cs.exposure,
            verified_exposure: cs.verified_exposure,
            blocked_amount: cs.blocked_amount,
            customer_name: cs.customer.name,
            customer_id: cs.customer.customer_id,
            investigator: cs.handler,
            incident_date: cs.incident_date,
            platform: cs.platform,
            original_report: cs.description,
            confirmed_evidence: (cs.evidence || []).filter(function(e) { return e.status === 'Confirmed'; }).map(function(e) {
                return { id: e.id, title: e.title, classification: e.classification, extracted_info: e.extracted_info, sha256: e.sha256 };
            }),
            confirmed_findings: (cs.findings || []).filter(function(f) { return f.status === 'Confirmed'; }).map(function(f) {
                return { id: f.id, title: f.title, description: f.description, confidence: f.confidence };
            }),
            partner_responses: (cs.partner_requests || []).filter(function(p) { return p.response; }).map(function(p) {
                return { partner: p.partner, result: p.response.verification_result, held_amount: p.response.held_amount, details: p.response.details };
            }),
            cyber_indicators: (cs.cyber && cs.cyber.indicators) ? cs.cyber.indicators.map(function(i) {
                return { type: i.type, value: i.value, classification: i.classification };
            }) : [],
            risk_history: cs.risk_history,
            decision: cs.decision
        };
    };

    // 4. Generative Intelligence 13-Mode Engine (Sections 21 & O.2)
    c.generateSelectedIntelligence = function() {
        c.genAILoading = true;
        var ctx = c.buildFNXCaseContext();
        var mode = c.selectedGenAIMode || 'journey';

        $timeout(function() {
            c.genAILoading = false;
            if (mode === 'journey') {
                c.generatedOutput = "=== CASE JOURNEY SUMMARY (END-TO-END) ===\\n\\n" +
                    "1. INTAKE & SUBMISSION:\\n" +
                    "Customer " + ctx.customer_name + " (" + ctx.customer_id + ") reported an unauthorized UPI fund debit of INR " + ctx.reported_exposure + " occurring on " + ctx.incident_date + " via " + ctx.platform + ".\\n\\n" +
                    "2. JOREN MULTIMODAL INTELLIGENCE:\\n" +
                    "Four evidence artifacts (SMS screenshot, URL screenshot, statement PDF, confirmation email) were ingested. Cryptographic SHA256 integrity was established. JOREN vision and web parsers classified the smishing SMS (VK-HDFCBK) and credential harvesting domain (secure-bank-login-verify.com).\\n\\n" +
                    "3. INVESTIGATOR VERIFICATION:\\n" +
                    "Forensic investigator " + ctx.investigator + " human-verified all 4 evidence records and confirmed 4 primary findings establishing credential capture and foreign Tor IP session hijacking (185.220.101.5).\\n\\n" +
                    "4. INTER-BANK PARTNER TRACE:\\n" +
                    "Partner Bank A completed verification request PR-001, confirming the unauthorized status of transaction UPI/2026/84920194819. A destination account lien of INR 35,000 has been placed on the beneficiary mule (pay-fast-merchant@ybl).\\n\\n" +
                    "5. RISK EVOLUTION & OUTCOME:\\n" +
                    "Case risk escalated from Initial (55) to Critical (" + ctx.risk_score + "/100). Manager approval granted by Marcus Vance. Reversal claim advice dispatched. Case disposition: Confirmed Fraud.";
            } else if (mode === 'status') {
                c.generatedOutput = "=== CURRENT STATUS SUMMARY ===\\n\\n" +
                    "• Case ID: " + ctx.case_number + "\\n" +
                    "• Status: " + ctx.current_status + " (SLA Remaining: 3h 45m)\\n" +
                    "• Risk Score: " + ctx.risk_score + "/100 (" + ctx.risk_level + ")\\n" +
                    "• Financial Loss: Reported INR " + ctx.reported_exposure + " | Verified INR " + ctx.verified_exposure + "\\n" +
                    "• Funds In Lien: INR " + ctx.blocked_amount + " (Recovery Pending)\\n" +
                    "• Evidence Items: " + ctx.confirmed_evidence.length + " Verified\\n" +
                    "• Confirmed Findings: " + ctx.confirmed_findings.length + " Confirmed\\n" +
                    "• Partner Status: Partner Bank A Verified (Lien Enacted)";
            } else if (mode === 'financial') {
                c.generatedOutput = "=== FINANCIAL INVESTIGATION SUMMARY ===\\n\\n" +
                    "• Remitter: Rajesh Sharma (Acct XXXX-XXXX-4819, Partner Bank A)\\n" +
                    "• Transaction Ref: UPI/2026/84920194819\\n" +
                    "• Gross Debited Amount: INR 85,000.00\\n" +
                    "• Beneficiary: pay-fast-merchant@ybl (Yes Bank Switch)\\n" +
                    "• Amount Blocked: INR 35,000.00 (Held under fraud lien)\\n" +
                    "• Outstanding Exposure: INR 50,000.00\\n" +
                    "• Regulatory Provision: RBI Zero-Liability Protection applied.";
            } else if (mode === 'cyber') {
                c.generatedOutput = "=== CYBER FORENSIC & ATTACK CHAIN SUMMARY ===\\n\\n" +
                    "• Attack Vector: Targeted Smishing (Sender ID: VK-HDFCBK)\\n" +
                    "• Phishing URL: hxxps://secure-bank-login-verify.com/login\\n" +
                    "• Attacker Session IP: 185.220.101.5 (Tor Exit Node, AS60729)\\n" +
                    "• Attack Chain: SMS -> Bitly Redirect -> Credential Harvesting Portal -> Automated Session Hijack -> High-Velocity UPI Transfer.\\n" +
                    "• Known Syndicate Link: Cluster Fake-Bank-Smish-2026.";
            } else if (mode === 'resolution_draft') {
                c.generatedOutput = "=== RESOLUTION NOTES DRAFT ===\\n\\n" +
                    "The forensic investigation has concluded that Case " + ctx.case_number + " represents unauthorized financial cyber fraud resulting from a targeted smishing campaign. All submitted evidence and IOCs have been validated. Partner Bank A has verified the unauthorized transfer and secured INR 35,000. A zero-liability claim has been initiated for full victim reimbursement. Case marked as RESOLVED (Confirmed Fraud).";
            } else {
                c.generatedOutput = "=== " + mode.toUpperCase() + " SUMMARY ===\\n\\n" +
                    "Analytical synthesis generated for Case " + ctx.case_number + ". Evaluated " + ctx.confirmed_evidence.length + " evidence items, " + ctx.confirmed_findings.length + " findings, and inter-bank partner verification. All attributes validate against established fraud indicators.";
            }
        }, 500);
    };

    // 5. Verification Workspace Navigation & Tabs
    c.setInvestigationTab = function(tabName) {
        c.investigationTab = tabName;
    };

    c.getRiskLabel = function(score) {
        var s = parseInt(score || 94, 10);
        if (s >= 85) return 'CRITICAL';
        if (s >= 70) return 'HIGH';
        if (s >= 50) return 'MEDIUM';
        return 'LOW';
    };

    c.getPendingVerificationCount = function() {
        if (!c.activeInvestigationCase) return 0;
        var pendingEv = (c.activeInvestigationCase.evidence || []).filter(function(e) { return e.status === 'Needs Review'; }).length;
        var pendingFnd = (c.activeInvestigationCase.findings || []).filter(function(f) { return f.status === 'Needs Review'; }).length;
        return pendingEv + pendingFnd;
    };

    c.isEvidenceVerified = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.evidence) return true;
        return c.activeInvestigationCase.evidence.every(function(e) { return e.status === 'Confirmed' || e.status === 'Rejected'; });
    };

    c.isFindingsConfirmed = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.findings) return true;
        return c.activeInvestigationCase.findings.every(function(f) { return f.status === 'Confirmed' || f.status === 'Rejected'; });
    };

    c.isPartnerVerified = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.partner_requests) return false;
        return c.activeInvestigationCase.partner_requests.some(function(p) { return p.status === 'Response Received' && p.analysis_accepted; });
    };

    // 6. Evidence & Findings Verification Actions
    c.confirmEvidence = function(ev) {
        ev.status = 'Confirmed';
        c.addTimelineEvent('HUMAN', 'Evidence Verified', 'Investigator Alex Morgan human-verified artifact ' + ev.id + ' (' + ev.title + ').', ev.id);
    };

    c.rejectEvidence = function(ev) {
        ev.status = 'Rejected';
        c.addTimelineEvent('HUMAN', 'Evidence Rejected', 'Investigator rejected artifact ' + ev.id + ' as non-contributory.', ev.id);
    };

    c.confirmAllEvidence = function() {
        (c.activeInvestigationCase.evidence || []).forEach(function(e) { e.status = 'Confirmed'; });
        c.addTimelineEvent('HUMAN', 'Batch Evidence Verification', 'All 4 evidence artifacts verified by investigator.', 'EV-ALL');
    };

    c.confirmFinding = function(fnd) {
        fnd.status = 'Confirmed';
        fnd.reviewer = 'Alex Morgan';
        fnd.reviewed_on = new Date().toLocaleTimeString();
        c.addTimelineEvent('HUMAN', 'Finding Confirmed', 'Investigator confirmed intelligence finding ' + fnd.id + '.', fnd.id);
    };

    c.rejectFinding = function(fnd) {
        fnd.status = 'Rejected';
        c.addTimelineEvent('HUMAN', 'Finding Rejected', 'Investigator rejected finding ' + fnd.id + '.', fnd.id);
    };

    c.confirmAllFindings = function() {
        (c.activeInvestigationCase.findings || []).forEach(function(f) {
            f.status = 'Confirmed';
            f.reviewer = 'Alex Morgan';
            f.reviewed_on = new Date().toLocaleTimeString();
        });
        c.addTimelineEvent('HUMAN', 'Batch Findings Confirmation', 'All intelligence findings confirmed by investigator.', 'FND-ALL');
    };

    
    // Verification Workspace Helpers
    c.setVerificationFilter = function(filter) {
        c.verificationQueueFilter = filter;
    };

    c.verifyEntity = function(ind) {
        ind.verified = !ind.verified;
        c.addTimelineEvent('HUMAN', 'Entity Verified', 'Investigator verified graph entity: ' + ind.type + ' (' + ind.value + ')', ind.value);
    };

    c.resetVerificationQueue = function() {
        if (!c.activeInvestigationCase) return;
        (c.activeInvestigationCase.evidence || []).forEach(function(e) {
            e.status = 'Needs Review';
        });
        (c.activeInvestigationCase.findings || []).forEach(function(f) {
            f.status = 'Needs Review';
            f.reviewer = 'Pending Human Review';
            f.reviewed_on = null;
        });
        if (c.activeInvestigationCase.cyber && c.activeInvestigationCase.cyber.indicators) {
            c.activeInvestigationCase.cyber.indicators.forEach(function(i) {
                i.verified = false;
            });
        }
        c.activeInvestigationCase.decision = { status: 'Pending', outcome: 'Under Review' };
        c.addTimelineEvent('SYSTEM', 'Verification Queue Reset', 'All evidence artifacts and findings reset to Needs Review for testing.', 'SYS-RESET');
        alert('Verification Queue reset! All 4 evidence artifacts and 4 findings are now pending human review.');
    };

    c.confirmAllPending = function() {
        c.confirmAllEvidence();
        c.confirmAllFindings();
    };

    // 7. Partner Verification
    c.openPartnerReqModal = function() {
        c.partnerForm = {
            partner: 'Partner Bank A - SIMULATED DEMO PARTNER',
            request_type: 'Transaction Verification',
            priority: 'P1 - Critical',
            due_date: '2026-10-02 18:00 IST',
            evidence_ref: 'EV-003 - Bank Statement PDF',
            description: 'Transaction TXN-2026-84920194819 for INR 85,000 requires inter-bank verification and beneficiary lien placement.'
        };
        c.showPartnerReqModal = true;
    };

    c.submitPartnerVerificationRequest = function() {
        var newReq = {
            id: 'PR-00' + (c.activeInvestigationCase.partner_requests.length + 1),
            partner: c.partnerForm.partner,
            demo_flag: true,
            request_type: c.partnerForm.request_type,
            priority: c.partnerForm.priority,
            due_date: c.partnerForm.due_date,
            description: c.partnerForm.description,
            status: 'Submitted'
        };
        c.activeInvestigationCase.partner_requests.unshift(newReq);
        c.showPartnerReqModal = false;
        c.addTimelineEvent('HUMAN', 'Partner Request Submitted', 'Inter-bank verification request sent to ' + newReq.partner, newReq.id);

        // Simulate instant demo partner response
        $timeout(function() {
            newReq.status = 'Response Received';
            newReq.response = {
                received_on: 'Just now',
                verification_result: 'CONFIRMED UNAUTHORIZED / SUSPECTED MULE NODE',
                details: 'Partner bank verifies unauthorized transaction sequence. Immediate debit freeze placed on beneficiary account pay-fast-merchant@ybl.',
                beneficiary_bank: 'Yes Bank Switch',
                account_status: 'FROZEN / LIEN PLACED',
                held_amount: 35000
            };
            newReq.ai_analysis = {
                classification: 'Confirms Unauthorized Transaction & Money Mule Account',
                supporting_info: 'Beneficiary account held INR 35,000. Rapid burst velocity indicates automated laundering.',
                contradictions: null,
                suggested_finding_update: 'FND-004: Beneficiary confirmed as flagged mule.',
                suggested_risk_impact: 'Elevate Case Risk to 94/100 (Critical)'
            };
            newReq.analysis_accepted = false;
            c.addTimelineEvent('SYSTEM', 'Partner Response Received', 'Simulated partner response received from ' + newReq.partner, newReq.id);
        }, 1200);
    };

    c.acceptPartnerAnalysis = function(pr) {
        pr.analysis_accepted = true;
        c.activeInvestigationCase.risk_score = 94;
        c.activeInvestigationCase.blocked_amount = 35000;
        c.addTimelineEvent('HUMAN', 'Partner Analysis Accepted', 'Investigator accepted partner analysis and elevated case risk to 94/100.', pr.id);
    };

    c.rejectPartnerAnalysis = function(pr) {
        pr.analysis_accepted = false;
        c.addTimelineEvent('HUMAN', 'Partner Analysis Rejected', 'Investigator rejected suggested risk elevation.', pr.id);
    };

    // 8. Alerts Modals
    c.openAlertCustomerModal = function() {
        c.customerAlertTemplate = 'case_update';
        c.onCustomerTemplateChange();
        c.showAlertCustomerModal = true;
    };

    c.onCustomerTemplateChange = function() {
        var t = c.customerAlertTemplate;
        var name = (c.activeInvestigationCase.customer && c.activeInvestigationCase.customer.name) || 'Customer';
        var num = c.activeInvestigationCase.number;
        if (t === 'case_received') {
            c.customerAlertPreview = 'Dear ' + name + ', your fraud report has been received and registered under Reference ' + num + '. Our Fraud Investigation Team is actively reviewing your evidence.';
        } else if (t === 'investigation_started') {
            c.customerAlertPreview = 'Dear ' + name + ', an official investigation has begun for case ' + num + '. Senior Investigator Alex Morgan has been assigned to lead your case.';
        } else if (t === 'case_update') {
            c.customerAlertPreview = 'Dear ' + name + ', update on Case ' + num + ': Our team has verified the unauthorized transaction with the destination bank and placed a lien on recipient funds. Next update in 2 hours.';
        } else if (t === 'decision_complete' || t === 'report_available') {
            c.customerAlertPreview = 'Dear ' + name + ', the investigation for Case ' + num + ' has concluded with an official finding of Confirmed Unauthorized Fraud. Zero-liability claim reimbursement advice has been issued. View your safe statement in the portal.';
        } else {
            c.customerAlertPreview = 'Dear ' + name + ', your case ' + num + ' has been updated by your investigation officer.';
        }
    };

    c.sendCustomerAlert = function() {
        c.showAlertCustomerModal = false;
        c.addTimelineEvent('HUMAN', 'Customer Alert Sent', 'Sanitized progress statement dispatched to ' + c.activeInvestigationCase.customer.email, 'NOTIF-CUST');
        alert('Safe notification dispatched to customer: ' + c.activeInvestigationCase.customer.email);
    };

    c.openAlertWorkerModal = function() {
        c.workerAlertTemplate = 'partner_response';
        c.workerAlertAssignee = 'Marcus Vance';
        c.workerAlertNotes = 'Partner Bank A confirmed unauthorized transaction. High exposure exceeds INR 50,000 threshold. Requesting manager review.';
        c.showAlertWorkerModal = true;
    };

    c.sendWorkerAlert = function() {
        c.showAlertWorkerModal = false;
        c.addTimelineEvent('HUMAN', 'Case Worker Alerted', 'Internal priority alert sent to ' + c.workerAlertAssignee + ': ' + c.workerAlertNotes, 'NOTIF-WRK');
        alert('Internal alert dispatched to ' + c.workerAlertAssignee);
    };

    // 9. Human Decision & Case Resolution
    c.decisionForm = {
        decision: 'Resolve Case',
        reason: 'Investigation confirms credentials were harvested via deceptive smishing domain secure-bank-login-verify.com. The unauthorized debit of INR 85,000 on 2026-10-02 has been verified by Partner Bank A. A lien of INR 35,000 is active on the beneficiary node. Reversal advice initiated.'
    };

    c.grantManagerApproval = function() {
        c.activeInvestigationCase.manager_approved = true;
        c.addTimelineEvent('HUMAN', 'Manager Approval Granted', 'Marcus Vance (Fraud Operations Director) authorized case resolution and claim advice.', 'APP-MV');
    };

    c.executeHumanDecision = function() {
        if (!c.isEvidenceVerified() || !c.isFindingsConfirmed()) {
            alert('Validation Error: All evidence items must be verified and findings confirmed before submitting resolution.');
            return;
        }
        if (!c.decisionForm.reason || c.decisionForm.reason.length < 15) {
            alert('Validation Error: A detailed formal decision reason is mandatory.');
            return;
        }

        c.activeInvestigationCase.decision = {
            status: 'Resolved',
            outcome: 'Confirmed Fraud',
            reason: c.decisionForm.reason,
            investigator: 'Alex Morgan',
            timestamp: new Date().toLocaleString()
        };
        c.activeInvestigationCase.status = 'Resolved';
        c.addTimelineEvent('HUMAN', 'Case Resolved', 'Formal human investigation decision executed: Confirmed Fraud. Case resolved.', c.activeInvestigationCase.number);
        alert('Human decision successfully recorded! Case ' + c.activeInvestigationCase.number + ' has been marked as RESOLVED.');
    };

    // 10. Generative Intelligence Review Actions
    c.openGenAIModal = function() {
        c.showGenAIModal = true;
        if (!c.generatedOutput) {
            c.generateSelectedIntelligence();
        }
    };

    c.acceptGenAI = function() {
        c.showGenAIModal = false;
        c.addTimelineEvent('HUMAN', 'Generative Intelligence Accepted', 'Investigator reviewed and accepted ' + c.selectedGenAIMode + ' synthesis.', 'GENAI-ACC');
        alert('Generative Intelligence synthesis accepted and attached to case dossier.');
    };

    c.rejectGenAI = function() {
        c.generatedOutput = '';
        c.showGenAIModal = false;
        c.addTimelineEvent('HUMAN', 'Generative Intelligence Rejected', 'Investigator rejected AI synthesis.', 'GENAI-REJ');
    };

    c.copyGenAIToReport = function() {
        c.showGenAIModal = false;
        c.setInvestigationTab('report');
        alert('Synthesis copied to Case Reports workspace.');
    };

    c.addGenAIToNotes = function() {
        c.activeInvestigationCase.notes.unshift({
            author: 'Alex Morgan (via GenAI)',
            role: 'Senior Investigator',
            timestamp: new Date().toLocaleTimeString(),
            text: c.generatedOutput,
            tags: ['GenAI', 'Synthesis']
        });
        c.showGenAIModal = false;
        c.setInvestigationTab('investigation');
    };

    // 11. Timeline Helper & Filtering
    c.addTimelineEvent = function(actorType, action, desc, recId) {
        var now = new Date();
        var timeStr = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0') + ' IST';
        c.activeInvestigationCase.timeline.unshift({
            time: timeStr,
            actor: actorType === 'HUMAN' ? 'Alex Morgan' : (actorType === 'AI SYSTEM' ? 'FRAUDNEXUS AI' : 'System Engine'),
            actor_type: actorType,
            action: action,
            desc: desc,
            record_id: recId
        });
    };

    c.getFilteredTimeline = function() {
        if (!c.activeInvestigationCase || !c.activeInvestigationCase.timeline) return [];
        if (!c.timelineFilter || c.timelineFilter === 'all') return c.activeInvestigationCase.timeline;
        return c.activeInvestigationCase.timeline.filter(function(item) {
            return item.actor_type === c.timelineFilter;
        });
    };

    // 12. End-to-End Demo Walkthrough (Section 35 & 40)
    c.demoWalkthroughActive = false;
    c.demoStep = 1;

    c.runEndToEndDemo = function() {
        c.demoWalkthroughActive = true;
        c.demoStep = 1;
        c.demoTitle = "1. Customer Submission Ingested";
        c.demoDesc = "Customer Rajesh Sharma reports INR 85,000 lost via smishing SMS. JOREN multimodal pipeline ingested 4 artifacts.";
        c.investigationTab = 'overview';
    c.verificationQueueFilter = 'all';
    };

    c.advanceDemo = function() {
        c.demoStep++;
        if (c.demoStep === 2) {
            c.demoTitle = "2. JOREN Multimodal Evidence Processing";
            c.demoDesc = "JOREN classifies SMS screenshot, URL capture, statement PDF, and email alert. Integrity hashes validated.";
            c.investigationTab = 'evidence';
        } else if (c.demoStep === 3) {
            c.demoTitle = "3. Human Verification of Evidence";
            c.demoDesc = "Investigator reviews and confirms all 4 submitted evidence artifacts.";
            c.confirmAllEvidence();
            c.investigationTab = 'verification';
        } else if (c.demoStep === 4) {
            c.demoTitle = "4. AI Findings Confirmation";
            c.demoDesc = "Investigator validates 4 AI-generated findings (credential harvesting, foreign IP session hijack, money mule).";
            c.confirmAllFindings();
            c.investigationTab = 'findings';
        } else if (c.demoStep === 5) {
            c.demoTitle = "5. Cyber Attack Chain Visualized";
            c.demoDesc = "Connected threat chain: Phishing SMS -> Fake Portal -> Harvested Credentials -> Tor IP 185.220.101.5 -> UPI Debit.";
            c.investigationTab = 'cyber';
        } else if (c.demoStep === 6) {
            c.demoTitle = "6. Inter-Bank Partner Request";
            c.demoDesc = "Submitted trace PR-001 to Partner Bank A (SIMULATED DEMO PARTNER).";
            c.investigationTab = 'partnerRequests';
        } else if (c.demoStep === 7) {
            c.demoTitle = "7. Partner Response & AI Analysis";
            c.demoDesc = "Partner Bank A confirms unauthorized debit; places lien on INR 35,000. Risk elevated to 94/100 Critical.";
            c.activeInvestigationCase.risk_score = 94;
            c.investigationTab = 'partnerRequests';
        } else if (c.demoStep === 8) {
            c.demoTitle = "8. Generative Intelligence Synthesis";
            c.demoDesc = "Generated comprehensive Case Journey Summary using FNXCaseContextBuilder.";
            c.openGenAIModal();
        } else if (c.demoStep === 9) {
            c.demoTitle = "9. Formal Human Decision & Manager Approval";
            c.demoDesc = "Investigator Alex Morgan records Confirmed Fraud resolution; Director Marcus Vance approves zero-liability claim.";
            c.grantManagerApproval();
            c.investigationTab = 'decision';
        } else if (c.demoStep === 10) {
            c.demoTitle = "10. Reports Dispatched & Case Resolved!";
            c.demoDesc = "Internal 27-section dossier compiled. Sanitized 13-section safe report dispatched to victim. Case Resolved!";
            c.executeHumanDecision();
            c.investigationTab = 'report';
        } else {
            c.demoWalkthroughActive = false;
        }
    };

    c.resetDemo = function() {
        c.activeInvestigationCase = c.setupDefaultInvestigationCase();
        c.demoStep = 1;
        c.runEndToEndDemo();
    };

    // 13. Initialize Active Case
    if (!c.activeInvestigationCase) {
        c.activeInvestigationCase = c.setupDefaultInvestigationCase();
    }
"""

with open('d:/KPMG/verification_workspace_client.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated verification_workspace_client.js, length: {len(js_content)}")
