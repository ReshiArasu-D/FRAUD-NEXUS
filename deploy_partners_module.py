"""
Deploy Partners Module to FRAUDNEXUS Unified ServiceNow Widget
"""
import requests
import json
import re

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
widget_id = "2f258577c32b43d0e54832f1b401317f"

print("==================================================")
print("PREPARING PARTNERS MODULE DEPLOYMENT")
print("==================================================")

# 1. READ SOURCE FILES
with open('live_widget_template.html', 'r', encoding='utf-8') as f:
    template = f.read()

with open('live_widget_client.js', 'r', encoding='utf-8') as f:
    client_script = f.read()

with open('live_widget_css.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('partner_template.html', 'r', encoding='utf-8') as f:
    partner_template = f.read()

with open('partner_styles.css', 'r', encoding='utf-8') as f:
    partner_styles = f.read()

with open('partner_client_methods.js', 'r', encoding='utf-8') as f:
    partner_methods = f.read()

# ----------------------------------------------------
# 2. PATCH TEMPLATE
# ----------------------------------------------------
print("1. Patching HTML Template...")

# 2a. Update Sidebar: Add Partners as module #5
sidebar_investigation = """                <!-- 4. Investigation -->
                <button class="fnx-sidebar-item" ng-class="{'active': c.adminModule === 'investigation'}" ng-click="c.setAdminModule('investigation')">
                    <span class="fnx-sidebar-icon">
                        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </span>
                    <span class="fnx-sidebar-label">{{c.t('investigation')}}</span>
                </button>"""

sidebar_partners = """                <!-- 4. Investigation -->
                <button class="fnx-sidebar-item" ng-class="{'active': c.adminModule === 'investigation'}" ng-click="c.setAdminModule('investigation')">
                    <span class="fnx-sidebar-icon">
                        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </span>
                    <span class="fnx-sidebar-label">{{c.t('investigation')}}</span>
                </button>

                <!-- 5. Partners -->
                <button class="fnx-sidebar-item" ng-class="{'active': c.adminModule === 'partners'}" ng-click="c.setAdminModule('partners')">
                    <span class="fnx-sidebar-icon">
                        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                    </span>
                    <span class="fnx-sidebar-label">{{c.t('partners') || 'Partners'}}</span>
                    <span class="fnx-sidebar-pill" style="background:rgba(0,184,217,0.15);color:#00B8D9;border-color:rgba(0,184,217,0.3);" ng-if="c.partnerKpis.total_partners">{{c.partnerKpis.total_partners}}</span>
                </button>"""

if "<!-- 5. Partners -->" not in template:
    template = template.replace(sidebar_investigation, sidebar_partners)
    print("  [OK] Sidebar updated with Partners module #5")
else:
    print("  [SKIP] Sidebar already contains Partners module")

# 2b. Add Investigation Workspace Partner Requests tab button
inv_tabs_orig = """                        <div class="fnx-inv-tabs">
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'overview'}" ng-click="c.setInvestigationTab('overview')">Overview</button>
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'evidence'}" ng-click="c.setInvestigationTab('evidence')">Evidence ({{c.activeInvestigationCase.evidence.length || 1}})</button>
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'tasks'}" ng-click="c.setInvestigationTab('tasks')">Tasks ({{c.activeInvestigationCase.tasks.length || 1}})</button>
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'timeline'}" ng-click="c.setInvestigationTab('timeline')">Timeline</button>
                        </div>"""

inv_tabs_new = """                        <div class="fnx-inv-tabs">
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'overview'}" ng-click="c.setInvestigationTab('overview')">Overview</button>
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'evidence'}" ng-click="c.setInvestigationTab('evidence')">Evidence ({{c.activeInvestigationCase.evidence.length || 1}})</button>
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'tasks'}" ng-click="c.setInvestigationTab('tasks')">Tasks ({{c.activeInvestigationCase.tasks.length || 1}})</button>
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'partnerRequests'}" ng-click="c.setInvestigationTab('partnerRequests')">Partner Requests ({{c.getCasePartnerRequests(c.activeInvestigationCase).length}})</button>
                            <button class="fnx-inv-tab" ng-class="{'active': c.investigationTab === 'timeline'}" ng-click="c.setInvestigationTab('timeline')">Timeline</button>
                        </div>"""

if "c.investigationTab === 'partnerRequests'" not in template:
    template = template.replace(inv_tabs_orig, inv_tabs_new)
    print("  [OK] Investigation workspace tab bar updated with Partner Requests tab")
else:
    print("  [SKIP] Investigation workspace tabs already contain Partner Requests tab")

# 2c. Add Investigation Workspace Partner Requests tab content
inv_tasks_content_end = """                                <button class="fnx-btn fnx-btn-outline fnx-btn-full" style="margin-top:1rem;" ng-click="c.openTaskModal(c.activeInvestigationCase)">+ Create Custom Investigation Task</button>
                            </div>
                        </div>"""

inv_partner_content = """                                <button class="fnx-btn fnx-btn-outline fnx-btn-full" style="margin-top:1rem;" ng-click="c.openTaskModal(c.activeInvestigationCase)">+ Create Custom Investigation Task</button>
                            </div>
                        </div>

                        <!-- TAB: PARTNER REQUESTS -->
                        <div ng-if="c.investigationTab === 'partnerRequests'" class="fnx-inv-tab-content fnx-inv-partner-tab">
                            <div class="fnx-card" style="margin-bottom:1.25rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                                    <div>
                                        <h3 style="font-size:1.1rem; font-weight:700; color:#0B1F3A; margin:0 0 4px 0;">CASE PARTNER COLLABORATION</h3>
                                        <p style="font-size:0.85rem; color:#64748B; margin:0;">Active external inter-agency requests linked to {{c.activeInvestigationCase.number}}</p>
                                    </div>
                                    <button class="fnx-btn fnx-btn-primary fnx-btn-sm" ng-click="c.openCreatePartnerRequest(null, c.activeInvestigationCase.sys_id)">
                                        + Request Partner Assistance
                                    </button>
                                </div>

                                <div class="fnx-table-responsive">
                                    <table class="fnx-data-table">
                                        <thead>
                                            <tr>
                                                <th>REQ ID</th>
                                                <th>PARTNER</th>
                                                <th>TYPE</th>
                                                <th>STATUS</th>
                                                <th>DUE / DISPATCHED</th>
                                                <th>RESPONSE / NOTES</th>
                                                <th style="text-align:right;">ACTIONS</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr ng-repeat="crq in c.getCasePartnerRequests(c.activeInvestigationCase)">
                                                <td><span class="fnx-mono-tag">{{crq.request_number}}</span></td>
                                                <td>
                                                    <div style="font-weight:600; color:#0B1F3A;">{{crq.partner_name}}</div>
                                                    <div style="font-size:0.75rem; color:#64748B;">{{crq.partner_category}}</div>
                                                </td>
                                                <td><span class="fnx-req-type-pill">{{crq.request_type}}</span></td>
                                                <td><span class="fnx-req-status-badge" ng-class="'req-st-' + crq.status.toLowerCase().replace(' ', '-')">{{crq.status}}</span></td>
                                                <td><span style="font-size:0.8rem; color:#64748B;">{{crq.request_date | limitTo:10}}</span></td>
                                                <td>
                                                    <div style="max-width:220px; font-size:0.8rem; color:#334155; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                                                        {{crq.response || crq.description || 'Pending'}}
                                                    </div>
                                                </td>
                                                <td style="text-align:right;">
                                                    <div class="fnx-row-actions">
                                                        <button class="fnx-action-btn btn-view" ng-click="c.viewPartnerRequest(crq)">View</button>
                                                        <button ng-if="crq.status !== 'Response Received' && crq.status !== 'Completed'" class="fnx-action-btn btn-sim" ng-click="c.simulatePartnerResponse(crq)">Simulate</button>
                                                        <button ng-if="crq.status === 'Response Received'" class="fnx-action-btn btn-comp" ng-click="c.updatePartnerRequestStatus(crq, 'Completed')">Complete</button>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr ng-if="c.getCasePartnerRequests(c.activeInvestigationCase).length === 0">
                                                <td colspan="7" style="text-align:center; padding:2rem; color:#94A3B8;">
                                                    No partner requests linked to this case yet. Click "+ Request Partner Assistance" to dispatch a request to banks, payment gateways, or cyber partners.
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>"""

if "<!-- TAB: PARTNER REQUESTS -->" not in template:
    template = template.replace(inv_tasks_content_end, inv_partner_content)
    print("  [OK] Investigation workspace tab content added")
else:
    print("  [SKIP] Investigation workspace tab content already present")

# 2d. Insert Partners Workspace View right before Intelligence Workspace
intel_comment = "            <!-- ==========================================\n                 VIEW 5: INTELLIGENCE WORKSPACE"
if "fnx-partners-page" not in template:
    template = template.replace(intel_comment, partner_template + "\n\n" + intel_comment)
    print("  [OK] Partners workspace view and modals inserted into template")
else:
    print("  [SKIP] Partners workspace view already present in template")

# ----------------------------------------------------
# 3. PATCH CLIENT SCRIPT
# ----------------------------------------------------
print("\n2. Patching Client Script...")

# 3a. Add dictionary translations
dict_en_insert = """            partners: 'Partners',
            partnerDirectory: 'Partner Directory',
            addPartner: 'Add Partner',
            editPartner: 'Edit Partner',
            partnerRequests: 'Partner Requests',
            requestStatus: 'Request Status',
            partnerCategory: 'Partner Category',
            integrationType: 'Integration Type',
            active: 'Active',
            inactive: 'Inactive',
            suspended: 'Suspended',
            simulatedDemoPartner: 'Simulated Demo Partner',
            totalPartners: 'Total Partners',
            activePartners: 'Active Partners',
            pendingRequests: 'Pending Requests',
            awaitingResponse: 'Awaiting Response',
            overdueRequests: 'Overdue Requests',"""

dict_ta_insert = """            partners: 'கூட்டாளர்கள்',
            partnerDirectory: 'கூட்டாளர் அடைவு',
            addPartner: 'கூட்டாளர் சேர்க்க',
            editPartner: 'கூட்டாளர் திருத்து',
            partnerRequests: 'கூட்டாளர் கோரிக்கைகள்',
            requestStatus: 'கோரிக்கை நிலை',
            partnerCategory: 'கூட்டாளர் வகை',
            integrationType: 'இணைப்பு வகை',
            active: 'செயலில்',
            inactive: 'செயலற்றது',
            suspended: 'இடைநிறுத்தப்பட்டது',
            simulatedDemoPartner: 'போலி மாதிரி கூட்டாளர்',
            totalPartners: 'மொத்த கூட்டாளர்கள்',
            activePartners: 'செயலில் உள்ள கூட்டாளர்கள்',
            pendingRequests: 'நிலுவை கோரிக்கைகள்',
            awaitingResponse: 'பதிலுக்காக காத்திருப்பவை',
            overdueRequests: 'தாமதமான கோரிக்கைகள்',"""

if "partnerDirectory: 'Partner Directory'" not in client_script:
    client_script = client_script.replace("commandCenter: 'Command Center',", "commandCenter: 'Command Center',\n" + dict_en_insert)
    client_script = client_script.replace("commandCenter: 'கட்டளை மையம்',", "commandCenter: 'கட்டளை மையம்',\n" + dict_ta_insert)
    print("  [OK] English and Tamil translations added")
else:
    print("  [SKIP] Translations already present")

# 3b. Update c.setAdminModule to load partners
set_admin_mod_orig = "        if (mod === 'customers') c.loadAdminCustomers();"
set_admin_mod_new = "        if (mod === 'customers') c.loadAdminCustomers();\n        if (mod === 'partners') c.loadPartners();"

if "if (mod === 'partners') c.loadPartners();" not in client_script:
    client_script = client_script.replace(set_admin_mod_orig, set_admin_mod_new)
    print("  [OK] c.setAdminModule updated to handle 'partners'")
else:
    print("  [SKIP] c.setAdminModule already handles 'partners'")

# 3c. Load partners on login
login_orig = "                c.loadAdminDashboard();"
login_new = "                c.loadAdminDashboard();\n                c.loadPartners();"
if "c.loadAdminDashboard();\n                c.loadPartners();" not in client_script:
    client_script = client_script.replace(login_orig, login_new)
    print("  [OK] Added c.loadPartners() to admin login routines")

# 3d. Append partner methods
if "c.partnerTab = 'directory';" not in client_script:
    # Insert right before scrollToTop helper
    marker = "    // ---- SCROLL TO TOP HELPER"
    if marker in client_script:
        client_script = client_script.replace(marker, partner_methods + "\n\n" + marker)
    else:
        client_script = client_script.replace("    c.scrollToTop = function() {", partner_methods + "\n\n    c.scrollToTop = function() {")
    print("  [OK] Injected partner client methods and state")
else:
    print("  [SKIP] Partner client methods already present")

# ----------------------------------------------------
# 4. PATCH CSS
# ----------------------------------------------------
print("\n3. Patching CSS...")
if ".fnx-partners-page" not in css:
    css = css + "\n\n" + partner_styles
    print("  [OK] Appended partner styles to widget CSS")
else:
    print("  [SKIP] Partner styles already present in CSS")

# ----------------------------------------------------
# 5. DEPLOY TO SERVICENOW
# ----------------------------------------------------
print("\n4. Deploying to ServiceNow...")
payload = {
    "template": template,
    "client_script": client_script,
    "css": css
}

resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{widget_id}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json=payload
)

print(f"Deploy Response: HTTP {resp.status_code}")
if resp.status_code == 200:
    print("SUCCESS: Widget successfully updated with full Partners Module!")
else:
    print(f"ERROR: {resp.text[:400]}")
