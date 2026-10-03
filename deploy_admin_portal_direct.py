"""
Direct Deployer for FRAUDNEXUS Admin & Investigator Portal
Imports base widget components from deploy_customer_experience_master,
extends them in memory with Admin features, and updates sp_widget directly.
"""
import requests
import os
import sys
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv('d:/KPMG/.env')

url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
WIDGET_ID = "2f258577c32b43d0e54832f1b401317f"

print("--- 1. Loading Base Customer Experience Components ---")
import deploy_customer_experience_master as base

server_script = base.server_script
client_script = base.client_script
template = base.template
css = base.css

print(f"Base loaded: client_script={len(client_script)} chars, template={len(template)} chars, css={len(css)} chars")

# --- 2. EXTEND DICTIONARIES IN CLIENT SCRIPT ---
admin_dict_en = """            commandCenter: 'Command Center',
            customers: 'Customers',
            cases: 'Cases',
            investigation: 'Investigation',
            intelligenceWorkspace: 'Intelligence Workspace',
            analytics: 'Analytics',
            settings: 'Settings',
            adminLoginTitle: 'WELCOME BACK',
            adminLoginSub: 'Sign in to FRAUDNEXUS Investigation Workspace',
            signIn: 'SIGN IN',
            tryDemo: 'TRY DEMO',
            demoEnv: 'DEMO ENVIRONMENT',
            priorityQueue: 'PRIORITY INVESTIGATION QUEUE',
            actionCenter: 'ACTION CENTER',
            fraudTrends: 'FRAUD CASE TRENDS',
            financialExposureSummary: 'FINANCIAL EXPOSURE SUMMARY',
            recentActivity: 'RECENT ACTIVITY',
            newCases: 'NEW CASES',
            criticalCases: 'CRITICAL CASES',
            escalatedCases: 'ESCALATED CASES',
            pendingApprovals: 'PENDING APPROVALS',
            financialExposure: 'FINANCIAL EXPOSURE',
            unassigned: 'Unassigned',
            assign: 'Assign',
            openWorkspace: 'Open Workspace',
            requestEvidence: 'Request Evidence',
            escalate: 'Escalate',
            resolve: 'Resolve',
            closeCase: 'Close Case',
            addTask: 'Add Task',
"""

admin_dict_ta = """            commandCenter: 'கட்டளை மையம்',
            customers: 'வாடிக்கையாளர்கள்',
            cases: 'வழக்குகள்',
            investigation: 'விசாரணை தளம்',
            intelligenceWorkspace: 'புலனாய்வு நுண்ணறிவு தளம்',
            analytics: 'பகுப்பாய்வு',
            settings: 'அமைப்புகள்',
            adminLoginTitle: 'மீண்டும் வருக',
            adminLoginSub: 'FRAUDNEXUS புலனாய்வு பணியிடத்தில் உள்நுழையவும்',
            signIn: 'உள்நுழைக',
            tryDemo: 'டெமோ காண்க',
            demoEnv: 'டெமோ சூழல்',
            priorityQueue: 'முன்னுரிமை விசாரணை வரிசை',
            actionCenter: 'செயல் மையம்',
            fraudTrends: 'மோசடி போக்குகள்',
            financialExposureSummary: 'நிதி வெளிப்பாடு சுருக்கம்',
            recentActivity: 'சமீபத்திய செயல்பாடுகள்',
            newCases: 'புதிய வழக்குகள்',
            criticalCases: 'முக்கிய வழக்குகள்',
            escalatedCases: 'தீவிரப்படுத்தப்பட்டவை',
            pendingApprovals: 'நிலுவையில் உள்ளவை',
            financialExposure: 'நிதி வெளிப்பாடு',
            unassigned: 'ஒதுக்கப்படாதவை',
            assign: 'ஒதுக்கு',
            openWorkspace: 'பணியிடத்தை திறக்க',
            requestEvidence: 'ஆதாரம் கோருக',
            escalate: 'தீவிரப்படுத்துக',
            resolve: 'தீர்க்க',
            closeCase: 'வழக்கை முடிக்க',
            addTask: 'பணி சேர்க்க',
"""

client_script = client_script.replace("logout: 'Logout'", "logout: 'Logout',\n" + admin_dict_en)
client_script = client_script.replace("logout: 'லॉग அவுட்'", "logout: 'லॉग அவுட்',\n" + admin_dict_ta)

# --- 3. EXTEND CLIENT CONTROLLER METHODS ---
admin_controller_code = r"""
    // ============================================================
    // FRAUDNEXUS ADMIN / INVESTIGATOR PORTAL STATE & METHODS
    // ============================================================
    c.adminUser = null;
    c.isAdminDemo = false;
    c.adminModule = 'commandCenter';
    c.adminError = '';
    c.adminLoading = false;
    c.adminForm = { email: 'alex.morgan@fraudnexus.com', password: 'DemoPass123!', showPassword: false };
    c.adminDash = {
        stats: { newCases: 17, activeCases: 48, criticalCases: 6, escalatedCases: 9, pendingApprovals: 11, financialExposure: 2800000, blockedAmount: 620000, recoveredAmount: 380000, outstandingAmount: 1800000 },
        priority_queue: [],
        action_center: [],
        trends: {},
        recent_activity: [],
        last_updated: 'Just now'
    };
    c.queueFilter = 'all';
    c.adminCasesList = [];
    c.casesFilter = 'all';
    c.casesSearch = '';
    c.adminCustList = [];
    c.custSearch = '';
    c.activeAdminCase = null;
    c.activeInvestigationCase = null;
    c.investigationTab = 'overview';
    c.investigationCases = [];
    c.showCaseDetailModal = false;
    c.showAssignModal = false;
    c.showTaskModal = false;
    c.showEvidenceReqModal = false;
    c.showEscalateModal = false;
    c.showResolveModal = false;
    c.targetCaseForModal = null;
    c.modalFeedback = '';
    c.assigneeSelect = 'alex.morgan@fraudnexus.com';
    c.taskForm = { title: '', desc: '', priority: 'High', assignee: 'Alex Morgan' };
    c.evidenceReqNotes = '';
    c.escalateReason = '';
    c.resolveNotes = '';
    c.resolveOutcome = 'Confirmed Fraud';
    c.adminAIInput = '';
    c.adminAIMessages = [
        {
            sender: 'ai',
            text: 'Hello Alex! I am your FRAUDNEXUS Operational Assistant.\n\nI can retrieve unassigned cases, check critical alerts, report SLA breaches, and assist your operational investigation tasks.',
            suggestions: ['Show unassigned cases', 'How many critical cases are open?', 'Show cases approaching SLA', 'Show my cases']
        }
    ];

    c.goToAdminLogin = function() {
        c.currentView = 'adminLogin';
        c.adminError = '';
    };

    c.toggleAdminPassword = function() {
        c.adminForm.showPassword = !c.adminForm.showPassword;
    };

    c.doAdminLogin = function() {
        c.adminError = '';
        c.adminLoading = true;
        $http.post(API + '/admin_login', { email: c.adminForm.email, password: c.adminForm.password })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminUser = d.user;
                c.isAdminDemo = d.is_demo || false;
                c.currentView = 'adminWorkspace';
                c.adminModule = 'commandCenter';
                c.loadAdminDashboard();
            } else {
                c.adminError = d.error || 'Invalid investigator credentials.';
            }
            c.adminLoading = false;
        }, function(err) {
            c.adminError = (err.data && err.data.result && err.data.result.error) || 'Invalid investigator credentials.';
            c.adminLoading = false;
        });
    };

    c.doAdminDemoLogin = function() {
        c.adminError = '';
        c.adminLoading = true;
        $http.post(API + '/admin_login', { demo: true })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminUser = d.user;
                c.isAdminDemo = true;
                c.currentView = 'adminWorkspace';
                c.adminModule = 'commandCenter';
                c.loadAdminDashboard();
            } else {
                c.adminError = d.error || 'Unable to start demo session.';
            }
            c.adminLoading = false;
        }, function(err) {
            c.adminError = (err.data && err.data.result && err.data.result.error) || 'Unable to connect to demo account.';
            c.adminLoading = false;
        });
    };

    c.logoutAdmin = function() {
        c.adminUser = null;
        c.isAdminDemo = false;
        c.currentView = 'portalSelect';
    };

    c.setAdminModule = function(mod) {
        c.adminModule = mod;
        if (mod === 'commandCenter') c.loadAdminDashboard();
        if (mod === 'cases') c.loadAdminCases(c.casesFilter);
        if (mod === 'customers') c.loadAdminCustomers();
        if (mod === 'investigation') {
            if (!c.activeInvestigationCase && c.adminDash.priority_queue.length > 0) {
                c.openInvestigation(c.adminDash.priority_queue[0]);
            }
        }
    };

    c.loadAdminDashboard = function() {
        $http.get(API + '/admin_dashboard')
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminDash = d;
            }
        });
    };

    c.filterQueue = function(f) {
        c.queueFilter = f;
    };

    c.getFilteredQueue = function() {
        if (!c.adminDash || !c.adminDash.priority_queue) return [];
        if (c.queueFilter === 'all') return c.adminDash.priority_queue;
        return c.adminDash.priority_queue.filter(function(cs) {
            if (c.queueFilter === 'critical') return cs.severity === 'Critical';
            if (c.queueFilter === 'high_risk') return cs.risk >= 70;
            if (c.queueFilter === 'unassigned') return cs.handler === 'Unassigned';
            if (c.queueFilter === 'near_sla') return cs.sla.indexOf('1') !== -1 || cs.sla.indexOf('2') !== -1;
            if (c.queueFilter === 'escalated') return cs.status === 'Escalated';
            return true;
        });
    };

    c.loadAdminCases = function(f) {
        c.casesFilter = f || 'all';
        var url = API + '/admin_cases?filter=' + encodeURIComponent(c.casesFilter);
        if (c.casesSearch) url += '&search=' + encodeURIComponent(c.casesSearch);
        $http.get(url).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminCasesList = d.cases;
            }
        });
    };

    c.loadAdminCustomers = function() {
        var url = API + '/admin_customers';
        if (c.custSearch) url += '?search=' + encodeURIComponent(c.custSearch);
        $http.get(url).then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.adminCustList = d.customers;
            }
        });
    };

    c.viewCaseDetail = function(cs) {
        $http.get(API + '/admin_cases?case_id=' + cs.sys_id)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.activeAdminCase = d.case;
                c.showCaseDetailModal = true;
            }
        });
    };

    c.openInvestigation = function(cs) {
        c.adminModule = 'investigation';
        c.investigationTab = 'overview';
        $http.get(API + '/admin_cases?case_id=' + cs.sys_id)
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            if (d.success) {
                c.activeInvestigationCase = d.case;
            }
        });
    };

    c.setInvestigationTab = function(t) {
        c.investigationTab = t;
    };

    // Modal Triggers
    c.openAssignModal = function(cs) {
        c.targetCaseForModal = cs;
        c.showAssignModal = true;
        c.modalFeedback = '';
    };

    c.openTaskModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showTaskModal = true;
        c.taskForm = { title: '', desc: '', priority: 'High', assignee: 'Alex Morgan' };
        c.modalFeedback = '';
    };

    c.openEvidenceReqModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showEvidenceReqModal = true;
        c.evidenceReqNotes = '';
        c.modalFeedback = '';
    };

    c.openEscalateModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showEscalateModal = true;
        c.escalateReason = '';
        c.modalFeedback = '';
    };

    c.openResolveModal = function(cs) {
        c.targetCaseForModal = cs || c.activeInvestigationCase;
        c.showResolveModal = true;
        c.resolveNotes = '';
        c.resolveOutcome = 'Confirmed Fraud';
        c.modalFeedback = '';
    };

    // Operational Actions Execution
    c.executeAssign = function() {
        if (!c.targetCaseForModal) return;
        var hName = c.assigneeSelect === 'alex.morgan@fraudnexus.com' ? 'Alex Morgan' : 'Sophia Reynolds';
        $http.post(API + '/admin_cases', {
            action: 'assign',
            case_id: c.targetCaseForModal.sys_id,
            handler_id: '',
            handler_name: hName
        }).then(function(resp) {
            c.showAssignModal = false;
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase && c.activeInvestigationCase.sys_id === c.targetCaseForModal.sys_id) {
                c.openInvestigation(c.targetCaseForModal);
            }
        });
    };

    c.executeTaskCreation = function() {
        if (!c.targetCaseForModal || !c.taskForm.title) return;
        $http.post(API + '/admin_cases', {
            action: 'add_task',
            case_id: c.targetCaseForModal.sys_id,
            title: c.taskForm.title,
            description: c.taskForm.desc,
            priority: c.taskForm.priority
        }).then(function(resp) {
            c.showTaskModal = false;
            if (c.activeInvestigationCase && c.activeInvestigationCase.sys_id === c.targetCaseForModal.sys_id) {
                c.openInvestigation(c.targetCaseForModal);
            }
        });
    };

    c.executeEvidenceRequest = function() {
        if (!c.targetCaseForModal) return;
        $http.post(API + '/admin_cases', {
            action: 'request_evidence',
            case_id: c.targetCaseForModal.sys_id,
            notes: c.evidenceReqNotes
        }).then(function(resp) {
            c.showEvidenceReqModal = false;
            c.loadAdminDashboard();
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    c.executeEscalate = function() {
        if (!c.targetCaseForModal) return;
        $http.post(API + '/admin_cases', {
            action: 'escalate',
            case_id: c.targetCaseForModal.sys_id,
            reason: c.escalateReason
        }).then(function(resp) {
            c.showEscalateModal = false;
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    c.executeResolve = function() {
        if (!c.targetCaseForModal) return;
        $http.post(API + '/admin_cases', {
            action: 'resolve',
            case_id: c.targetCaseForModal.sys_id,
            outcome: c.resolveOutcome,
            notes: c.resolveNotes
        }).then(function(resp) {
            c.showResolveModal = false;
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    c.executeClose = function(cs) {
        var target = cs || c.activeInvestigationCase;
        if (!target) return;
        $http.post(API + '/admin_cases', {
            action: 'close',
            case_id: target.sys_id,
            notes: 'Investigation closed by authorized investigator.'
        }).then(function(resp) {
            c.loadAdminDashboard();
            if (c.adminModule === 'cases') c.loadAdminCases(c.casesFilter);
            if (c.activeInvestigationCase) c.openInvestigation(c.activeInvestigationCase);
        });
    };

    // Admin AI Interaction
    c.sendAdminAI = function(predefined) {
        var queryText = predefined || c.adminAIInput;
        if (!queryText || !queryText.trim()) return;
        c.adminAIMessages.push({ sender: 'user', text: queryText });
        c.adminAIInput = '';
        var curCaseId = (c.adminModule === 'investigation' && c.activeInvestigationCase) ? c.activeInvestigationCase.sys_id : '';

        $http.post(API + '/admin_ai', { query: queryText, current_case_id: curCaseId })
        .then(function(resp) {
            var d = resp.data.result || resp.data;
            c.adminAIMessages.push({
                sender: 'ai',
                text: d.reply,
                suggestions: d.suggestions || []
            });
        }, function(err) {
            c.adminAIMessages.push({
                sender: 'ai',
                text: 'Sorry, I encountered an operational query error. Please try again.',
                suggestions: ['Show unassigned cases', 'Show critical cases']
            });
        });
    };

    // Check URL parameters for direct view routing
    try {
        var qParams = new URLSearchParams($window.location.search);
        if (qParams.get('view') === 'admin' || qParams.get('admin') === 'true' || qParams.get('view') === 'adminLogin') {
            c.goToAdminLogin();
        }
    } catch(e) {}
"""

client_script = client_script.replace("    c.getStatusClass = function(s) {", admin_controller_code + "\n    c.getStatusClass = function(s) {")

# --- 4. EXTEND TEMPLATE ---
# Update Card 2 button in Portal Selection
old_card2_btn = """            <button class="fnx-btn fnx-btn-disabled fnx-btn-full" disabled>{{c.t('comingSoon')}}</button>"""
new_card2_btn = """            <!-- investigatorPortal comingSoon enabled for Admin / Investigator Portal -->
            <button class="fnx-btn fnx-btn-primary fnx-btn-full" ng-click="c.goToAdminLogin()">Enter Investigator Workspace &rarr;</button>"""
template = template.replace(old_card2_btn, new_card2_btn)

# Load admin template
with open('d:/KPMG/admin_template.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Append admin template before final </div> of the app
last_div = template.rfind("</div>")
if last_div != -1:
    template = template[:last_div] + "\n" + admin_html + "\n</div>"
    print("Injected admin_html before final </div>")
else:
    template = template + "\n" + admin_html

# --- 5. EXTEND CSS ---
with open('d:/KPMG/admin_styles.css', 'r', encoding='utf-8') as f:
    admin_css = f.read()

css = css + "\n\n" + admin_css

print(f"Final sizes: client_script={len(client_script)}, template={len(template)}, css={len(css)}")

# --- 6. UPLOAD WIDGET TO SERVICENOW ---
print("--- Uploading Unified Master Widget to ServiceNow ---")
widget_payload = {
    'template': template,
    'client_script': client_script,
    'script': server_script,
    'css': css
}

r = requests.patch(f"{url}/api/now/table/sp_widget/{WIDGET_ID}", auth=auth, headers=headers, json=widget_payload)
print(f"Deploy status: {r.status_code}")
if r.status_code == 200:
    print("SUCCESS: Master Customer + Admin Experience Widget successfully deployed to dev187180!")
else:
    print(f"FAILED: {r.text[:500]}")
