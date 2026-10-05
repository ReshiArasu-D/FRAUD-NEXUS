import requests

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'

# ======================================================
# STEP 1: Build patched client script with $timeout fix
# ======================================================
with open(r'd:\KPMG\client_script_backup.js', 'r', encoding='utf-8') as f:
    script = f.read()

# Add scrollToTop helper with $timeout
scroll_helper = (
    "    // ---- SCROLL TO TOP HELPER ($timeout ensures digest is complete first) ----\n"
    "    c.scrollToTop = function() {\n"
    "        $timeout(function() {\n"
    "            try {\n"
    "                // Try the fnx-app's own scroll container (view containers)\n"
    "                var targets = [\n"
    "                    document.querySelector('.fnx-landing'),\n"
    "                    document.querySelector('.fnx-portal-select-view'),\n"
    "                    document.querySelector('.fnx-admin-login-page'),\n"
    "                    document.querySelector('.fnx-admin-main-content'),\n"
    "                    document.querySelector('.sp-scroll'),\n"
    "                    document.querySelector('[class*=\"sp-col\"]'),\n"
    "                    document.querySelector('.panel-col-content'),\n"
    "                    document.documentElement,\n"
    "                    document.body\n"
    "                ];\n"
    "                for (var i = 0; i < targets.length; i++) {\n"
    "                    if (targets[i]) targets[i].scrollTop = 0;\n"
    "                }\n"
    "                window.scrollTo(0, 0);\n"
    "                window.scrollTo({ top: 0, left: 0, behavior: 'instant' });\n"
    "            } catch(e) {}\n"
    "        }, 50);\n"
    "    };\n\n"
)

script = script.replace(
    "    c.navigate = function(view) {",
    scroll_helper + "    c.navigate = function(view) {"
)

# Patch c.navigate
script = script.replace(
    "    c.navigate = function(view) {\n"
    "        if (view === 'reportFraud') { c.startNewReport(); return; }\n"
    "        if (view === 'trackCases') { c.loadCases(); }\n"
    "        if (view === 'editProfile') { c.initEditProfile(); }\n"
    "        c.currentView = view;\n"
    "    };",

    "    c.navigate = function(view) {\n"
    "        if (view === 'reportFraud') { c.startNewReport(); c.scrollToTop(); return; }\n"
    "        if (view === 'trackCases') { c.loadCases(); }\n"
    "        if (view === 'editProfile') { c.initEditProfile(); }\n"
    "        c.currentView = view;\n"
    "        c.scrollToTop();\n"
    "    };"
)

# Patch goToPortalSelect
script = script.replace(
    "    c.goToPortalSelect = function() { c.currentView = 'portalSelect'; };",
    "    c.goToPortalSelect = function() { c.currentView = 'portalSelect'; c.scrollToTop(); };"
)

# Patch goToAuth
script = script.replace(
    "    c.goToAuth = function() { c.currentView = 'auth'; c.authMode = 'login'; };",
    "    c.goToAuth = function() { c.currentView = 'auth'; c.authMode = 'login'; c.scrollToTop(); };"
)

# Patch goToAdminLogin
script = script.replace(
    "    c.goToAdminLogin = function() {\n"
    "        c.currentView = 'adminLogin';\n"
    "        c.adminError = '';\n"
    "    };",
    "    c.goToAdminLogin = function() {\n"
    "        c.currentView = 'adminLogin';\n"
    "        c.adminError = '';\n"
    "        c.scrollToTop();\n"
    "    };"
)

# Patch doAdminLogin success (regular login)
script = script.replace(
    "                c.adminUser = d.user;\n"
    "                c.isAdminDemo = d.is_demo || false;\n"
    "                c.currentView = 'adminWorkspace';\n"
    "                c.adminModule = 'commandCenter';\n"
    "                c.loadAdminDashboard();",
    "                c.adminUser = d.user;\n"
    "                c.isAdminDemo = d.is_demo || false;\n"
    "                c.currentView = 'adminWorkspace';\n"
    "                c.adminModule = 'commandCenter';\n"
    "                c.scrollToTop();\n"
    "                c.loadAdminDashboard();",
    1
)

# Patch doAdminDemoLogin success
script = script.replace(
    "                c.adminUser = d.user;\n"
    "                c.isAdminDemo = true;\n"
    "                c.currentView = 'adminWorkspace';\n"
    "                c.adminModule = 'commandCenter';\n"
    "                c.loadAdminDashboard();",
    "                c.adminUser = d.user;\n"
    "                c.isAdminDemo = true;\n"
    "                c.currentView = 'adminWorkspace';\n"
    "                c.adminModule = 'commandCenter';\n"
    "                c.scrollToTop();\n"
    "                c.loadAdminDashboard();",
    1
)

# Patch logoutAdmin
script = script.replace(
    "    c.logoutAdmin = function() {\n"
    "        c.adminUser = null;\n"
    "        c.isAdminDemo = false;\n"
    "        c.currentView = 'portalSelect';\n"
    "    };",
    "    c.logoutAdmin = function() {\n"
    "        c.adminUser = null;\n"
    "        c.isAdminDemo = false;\n"
    "        c.currentView = 'portalSelect';\n"
    "        c.scrollToTop();\n"
    "    };"
)

print("Client script patched. scrollToTop calls:", script.count("c.scrollToTop()"))

# ======================================================
# STEP 2: Build patched CSS
# Each view section is height:100vh + overflow:auto so it
# self-contains scrolling. The outer SP page never scrolls.
# ======================================================
with open(r'd:\KPMG\widget_css_backup.css', 'r', encoding='utf-8') as f:
    css = f.read()

scroll_architecture_css = """
/* =====================================================================
   SCROLL ARCHITECTURE FIX v2
   Each view is a self-contained scroll container (height:100vh, overflow:auto).
   The outer ServiceNow SP page NEVER scrolls — so switching views always
   starts at y=0 with no manual scroll reset needed.
   ===================================================================== */

/* Root app container: full viewport, no outer overflow */
.fnx-app {
    height: 100vh !important;
    overflow: hidden !important;
    position: relative !important;
}

/* Landing view scrolls internally */
.fnx-landing {
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    scroll-behavior: smooth !important;
}

/* Portal select view: self-contained */
.fnx-portal-select-view,
div[ng-if*="portalSelect"],
div[ng-if="c.currentView === 'portalSelect'"] {
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

/* Auth views (login, register etc): self-contained */
.fnx-auth-view,
div[ng-if="c.currentView === 'auth'"],
div[ng-if*="auth"] {
    height: 100vh !important;
    overflow-y: auto !important;
}

/* Admin login page: full viewport, no outer scroll */
.fnx-admin-login-page {
    height: 100vh !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    flex-shrink: 0 !important;
}

/* Admin workspace layout: full viewport, flex column */
.fnx-admin-layout {
    height: 100vh !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Admin topbar: sticky, never scrolls away */
.fnx-admin-topbar {
    flex-shrink: 0 !important;
    height: 64px !important;
    z-index: 100 !important;
}

/* Admin body: fills remaining space, overflow hidden (children scroll) */
.fnx-admin-body {
    flex: 1 1 auto !important;
    min-height: 0 !important;
    overflow: hidden !important;
    display: flex !important;
}

/* Admin sidebar: full height, scrolls internally */
.fnx-admin-sidebar {
    flex-shrink: 0 !important;
    height: 100% !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

/* Main content: the ONLY scrollable area in admin workspace */
.fnx-admin-main-content {
    flex: 1 1 auto !important;
    min-height: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: 100% !important;
    padding: 1.75rem 2rem !important;
    background-color: #F5F7FA !important;
}

/* Kill any SP bootstrap column/row padding that could create space */
.sp-widget-content,
.sp-widget-content > div {
    padding: 0 !important;
    margin: 0 !important;
}

/* =====================================================================
   END SCROLL ARCHITECTURE FIX
   ===================================================================== */

"""

# Insert after the first @import line
import_end = css.find('\n', css.find('@import'))
css_fixed = css[:import_end+1] + scroll_architecture_css + css[import_end+1:]

print("CSS patched, length:", len(css_fixed))

# ======================================================
# STEP 3: Deploy both to ServiceNow
# ======================================================
r = requests.patch(
    f'{base}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f',
    auth=auth,
    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    json={
        'client_script': script,
        'css': css_fixed
    }
)

print('PATCH status:', r.status_code)
if r.status_code == 200:
    print('SUCCESS: Widget deployed with scroll architecture fix!')
else:
    print('ERROR:', r.text[:500])
