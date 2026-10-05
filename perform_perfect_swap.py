import requests, sys, os, re, time

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=== PERFORMING SWAP AND RESTORE ===")

# 1. Fetch current live widget
print("1. Fetching live widget...")
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
live_tpl = data['template']
live_css = data['css']
live_cs = data['client_script']

# 2. Extract original Investigation module from working_template.html
print("2. Reading original Investigation module from working_template.html...")
with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    wt = f.read()

orig_inv_start = "<!-- ==========================================\n                 VIEW 4: INVESTIGATION WORKSPACE (Phase 1 Shell)\n                 ========================================== -->"
orig_inv_end = "<!-- ============================================================\n     FRAUDNEXUS ADMIN PORTAL — PARTNERS MODULE TEMPLATE"

s_idx = wt.find(orig_inv_start)
e_idx = wt.find(orig_inv_end)

if s_idx == -1 or e_idx == -1:
    print("ERROR: Could not locate original investigation module in working_template.html")
    sys.exit(1)

orig_inv_html = wt[s_idx:e_idx].strip()
print(f"Original Investigation HTML length: {len(orig_inv_html)}")

# 3. Read Verification Workspace template
print("3. Reading Verification Workspace template...")
with open('d:/KPMG/verification_workspace_template.html', 'r', encoding='utf-8') as f:
    vw_html = f.read()

# Change top div from c.adminModule === 'investigation' to c.adminModule === 'intelligence'
vw_html_wired = vw_html.replace(
    "<div ng-if=\"c.adminModule === 'investigation'\" class=\"fnx-investigation-workspace\">",
    "<div ng-if=\"c.adminModule === 'intelligence'\" class=\"fnx-investigation-workspace\">"
)
print(f"Verification Workspace HTML length: {len(vw_html_wired)}")

# 4. In live template:
# Part A: Replace the current Verification Workspace at c.adminModule === 'investigation' with original Investigation HTML
print("4. Restoring original Investigation module...")
current_vw_marker = "<!-- ============================================================\n     FRAUDNEXUS — FINAL ENTERPRISE VERIFICATION WORKSPACE"
partners_marker = "<!-- ============================================================\n     FRAUDNEXUS ADMIN PORTAL — PARTNERS MODULE TEMPLATE"

pos1 = live_tpl.find(current_vw_marker)
pos2 = live_tpl.find(partners_marker, pos1)

if pos1 == -1 or pos2 == -1:
    print(f"ERROR: Could not find markers for current VW in live template! pos1={pos1}, pos2={pos2}")
    sys.exit(1)

print(f"Replacing current VW (from {pos1} to {pos2}) with original Investigation module...")
tpl_after_restore = live_tpl[:pos1] + orig_inv_html + "\n\n            " + live_tpl[pos2:]

# Part B: Replace the placeholder shell at c.adminModule === 'intelligence' with the Verification Workspace
print("5. Wiring Verification Workspace to c.adminModule === 'intelligence'...")
intel_marker = "<div ng-if=\"c.adminModule === 'intelligence'\" class=\"fnx-admin-page-view\">"
analytics_marker = "<!-- ==========================================\n                 VIEW 6: ANALYTICS MODULE"

pos_intel = tpl_after_restore.find(intel_marker)
pos_analytics = tpl_after_restore.find(analytics_marker, pos_intel)

if pos_intel == -1 or pos_analytics == -1:
    print(f"ERROR: Could not find intel placeholder markers! pos_intel={pos_intel}, pos_analytics={pos_analytics}")
    sys.exit(1)

# Find the start of the comment before intel_marker
comment_before = "<!-- ==========================================\n                 VIEW 5: INTELLIGENCE WORKSPACE"
cb_pos = tpl_after_restore.rfind("<!--", 0, pos_intel)
if cb_pos != -1 and "VIEW 5" in tpl_after_restore[cb_pos:pos_intel]:
    intel_start = cb_pos
else:
    intel_start = pos_intel

print(f"Replacing placeholder (from {intel_start} to {pos_analytics}) with Verification Workspace...")
final_tpl = tpl_after_restore[:intel_start] + vw_html_wired + "\n\n            " + tpl_after_restore[pos_analytics:]

# Part C: Update the sidebar button label from Intelligence Workspace (Phase 2) to Verification Workspace (Live)
print("6. Updating Sidebar button label...")
old_sidebar_btn = """                <!-- 5. Intelligence Workspace (Shell) -->
                <button class="fnx-sidebar-item" ng-class="{'active': c.adminModule === 'intelligence'}" ng-click="c.setAdminModule('intelligence')">
                    <span class="fnx-sidebar-icon">
                        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
                    </span>
                    <span class="fnx-sidebar-label">{{c.t('intelligenceWorkspace')}}</span>
                    <span class="fnx-sidebar-pill">Phase 2</span>
                </button>"""

new_sidebar_btn = """                <!-- 5. Verification Workspace (Live Enterprise 3-Column) -->
                <button class="fnx-sidebar-item" ng-class="{'active': c.adminModule === 'intelligence'}" ng-click="c.setAdminModule('intelligence')">
                    <span class="fnx-sidebar-icon">
                        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    </span>
                    <span class="fnx-sidebar-label">Verification Workspace</span>
                    <span class="fnx-sidebar-pill" style="background:#E0F2FE;color:#0369A1;font-weight:700;">Live</span>
                </button>"""

if old_sidebar_btn in final_tpl:
    final_tpl = final_tpl.replace(old_sidebar_btn, new_sidebar_btn)
    print("Sidebar button updated cleanly.")
else:
    print("Replacing sidebar label via regex...")
    final_tpl = re.sub(
        r'<button class="fnx-sidebar-item" ng-class="\{\'active\': c\.adminModule === \'intelligence\'\}".*?</button>',
        new_sidebar_btn.strip(),
        final_tpl,
        flags=re.DOTALL
    )

# 7. Update Client Script to ensure setAdminModule initializes case for intelligence module
print("7. Updating Client Script for module initialization...")
if "if (mod === 'intelligence')" not in live_cs:
    init_snippet = """
        if (mod === 'intelligence') {
            if (!c.activeInvestigationCase) {
                c.activeInvestigationCase = c.setupDefaultInvestigationCase();
            }
            if (!c.investigationTab) {
                c.investigationTab = 'overview';
            }
        }
    """
    live_cs = live_cs.replace(
        "c.setAdminModule = function(mod) {",
        "c.setAdminModule = function(mod) {" + init_snippet
    )

# 8. Deploy to ServiceNow REST API
print("8. Deploying to ServiceNow widget...")
patch_resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'template': final_tpl, 'css': live_css, 'client_script': live_cs}
)

if patch_resp.status_code == 200:
    print("SUCCESS: Widget successfully updated!")
    print("Flushing cache...")
    requests.get(f'{base}/cache.do', auth=auth)
    print("Cache flushed successfully!")
else:
    print(f"ERROR: {patch_resp.status_code} - {patch_resp.text[:400]}")
    sys.exit(1)

print("=== SWAP AND RESTORE COMPLETED SUCCESSFULLY ===")
