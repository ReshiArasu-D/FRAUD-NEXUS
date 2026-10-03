"""
FRAUDNEXUS Master Deployer: Customer Portal + Admin / Investigator Portal
Preserves all existing Customer Portal logic, templates, and styles without breaking changes.
Adds:
- Admin Login (Navy/White 2-column layout, eye toggle, Sign In, Try Demo)
- Legitimate Demo Login (Alex Morgan seeded investigator)
- Admin Workspace Shell (Header with search, notifications, language, profile; Sidebar with exactly 7 modules)
- Command Center (6 KPIs, Priority Queue, Action Center, Trends, Exposure Summary, Recent Activity)
- Customer Management Foundation
- Case Management Foundation with all filters and actions
- Investigation Workspace Shell (3-column layout: Nav, 4 Tabs [Overview, Evidence, Tasks, Timeline], Actions)
- Intelligence Workspace Shell (Clean Phase 1 placeholder)
- Analytics Foundation Shell
- Settings Foundation
- Context-Aware Admin AI Assistant Drawer
"""
import requests
import os
import sys
import json
import re
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv('d:/KPMG/.env')

url = os.getenv('SERVICENOW_INSTANCE_URL')
auth = HTTPBasicAuth(os.getenv('SERVICENOW_USERNAME'), os.getenv('SERVICENOW_PASSWORD'))
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
WIDGET_ID = "2f258577c32b43d0e54832f1b401317f"

# Read base file
with open('d:/KPMG/deploy_customer_experience_master.py', 'r', encoding='utf-8') as f:
    master_code = f.read()

# 1. EXTEND DICTIONARIES
admin_dict_en = """
            commandCenter: 'Command Center',
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

admin_dict_ta = """
            commandCenter: 'கட்டளை மையம்',
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

# Insert into dictionary
master_code = master_code.replace("logout: 'Logout'", "logout: 'Logout',\n" + admin_dict_en)
master_code = master_code.replace("logout: 'லॉग அவுட்'", "logout: 'லॉग அவுட்',\n" + admin_dict_ta)

# 2. EXTEND CLIENT CONTROLLER (Admin state & methods)
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
        if (qParams.get('view') === 'admin' || qParams.get('admin') === 'true') {
            c.goToAdminLogin();
        }
    } catch(e) {}
"""

# Insert admin controller methods before closing of api.controller
master_code = master_code.replace("    c.getStatusClass = function(s) {", admin_controller_code + "\n    c.getStatusClass = function(s) {")

# 3. UPDATE PORTAL SELECTION CARD 2 (Investigator button)
old_card2_btn = """            <button class="fnx-btn fnx-btn-disabled fnx-btn-full" disabled>{{c.t('comingSoon')}}</button>"""
new_card2_btn = """            <button class="fnx-btn fnx-btn-primary fnx-btn-full" ng-click="c.goToAdminLogin()">Enter Investigator Workspace &rarr;</button>"""
master_code = master_code.replace(old_card2_btn, new_card2_btn)

# 4. LOAD AND APPEND ADMIN TEMPLATE
with open('d:/KPMG/admin_template.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Append admin template inside template string before the final closing </div>
master_code = master_code.replace("<!-- Google Fonts: Plus Jakarta Sans, Outfit, Inter -->", "<!-- Google Fonts: Plus Jakarta Sans, Outfit, Inter -->\n")
# Find last occurrence of </div> in template (before the closing quote)
pos = master_code.find('<!-- ============ 7. EVIDENCE VAULT VIEW ============ -->')
# We can cleanly append admin_html right before the end of the template string
template_marker = '<!-- ============ HELP / SUPPORT ============ -->'
pos_help = master_code.find(template_marker)
# Let's find the closing of the template raw string
pos_template_end = master_code.find('"""\n\n# 4. CSS STYLESHEET')
if pos_template_end == -1:
    pos_template_end = master_code.find("'''\n\n# 4. CSS STYLESHEET")
if pos_template_end == -1:
    # Look for css = r"""
    pos_template_end = master_code.find("css = r\"\"\"")

print("Found template end at:", pos_template_end)
if pos_template_end != -1:
    # Insert admin_html right before pos_template_end
    # We find the </div> right before pos_template_end
    master_code = master_code[:pos_template_end] + "\n" + admin_html + "\n" + master_code[pos_template_end:]
    print("Injected admin_html into master_code successfully!")
else:
    print("ERROR: Could not find template end marker!")
    sys.exit(1)

# 5. LOAD AND APPEND ADMIN CSS
with open('d:/KPMG/admin_styles.css', 'r', encoding='utf-8') as f:
    admin_css = f.read()

# Append admin CSS before the end of css string
css_end = master_code.rfind('"""\n\nprint("--- Uploading Master Widget Components to ServiceNow ---")')
if css_end == -1:
    css_end = master_code.rfind("'''\n\nprint(\"--- Uploading Master Widget Components to ServiceNow ---\")")

print("Found css end at:", css_end)
if css_end != -1:
    master_code = master_code[:css_end] + "\n" + admin_css + "\n" + master_code[css_end:]
    print("Injected admin_css into master_code successfully!")
else:
    print("ERROR: Could not find CSS end marker!")
    sys.exit(1)

# Write out deploy_master_with_admin.py
with open('d:/KPMG/deploy_master_with_admin.py', 'w', encoding='utf-8') as f:
    f.write(master_code)

print("Created d:/KPMG/deploy_master_with_admin.py successfully!")
