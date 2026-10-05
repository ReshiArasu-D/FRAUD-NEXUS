import requests, json

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'

with open(r'd:\KPMG\client_script_backup.js', 'r', encoding='utf-8') as f:
    script = f.read()

# Add scrollToTop helper just before c.navigate
scroll_helper = (
    "    // ---- SCROLL TO TOP HELPER (fixes blank-space on view change) ----\n"
    "    c.scrollToTop = function() {\n"
    "        try {\n"
    "            var containers = [\n"
    "                document.querySelector('.sp-scroll'),\n"
    "                document.querySelector('.page'),\n"
    "                document.querySelector('#sp-col-content'),\n"
    "                document.querySelector('.col-xs-12'),\n"
    "                document.body\n"
    "            ];\n"
    "            for (var i = 0; i < containers.length; i++) {\n"
    "                if (containers[i]) containers[i].scrollTop = 0;\n"
    "            }\n"
    "            window.scrollTo(0, 0);\n"
    "        } catch(e) {}\n"
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

# Patch doAdminLogin success (first occurrence - regular login)
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

with open(r'd:\KPMG\client_script_patched.js', 'w', encoding='utf-8') as f:
    f.write(script)

print('Script patched successfully')
print('Lines now:', len(script.split('\n')))

checks = ['c.scrollToTop = function', 'c.scrollToTop();']
for check in checks:
    count = script.count(check)
    print('  Occurrences of "{}": {}'.format(check, count))
