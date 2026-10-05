import requests

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'

# Load the patched client script
with open(r'd:\KPMG\client_script_patched.js', 'r', encoding='utf-8') as f:
    patched_client_script = f.read()

# Load the current CSS and add scroll-reset CSS fixes at the top
with open(r'd:\KPMG\widget_css_backup.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add CSS to nuke any SP-injected padding/margin on parent containers and ensure
# the admin workspace starts exactly at the top of its container
scroll_fix_css = """
/* ===================================================================
   SCROLL / BLANK-SPACE FIX
   Forces the fnx-app container and its SP wrapper to have no extra
   top padding so admin views render immediately at y=0.
   =================================================================== */

/* Kill any SP bootstrap container / row padding that causes blank space */
.fnx-app,
.fnx-app > *,
.fnx-landing,
.fnx-admin-login-page,
.fnx-admin-layout {
    box-sizing: border-box !important;
}

/* Ensure SP page container doesn't add spacing */
.sp-widget-content {
    padding: 0 !important;
    margin: 0 !important;
}

/* Admin layout must be flush to top */
.fnx-admin-layout {
    position: relative !important;
    top: 0 !important;
    left: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    overflow: hidden !important;
}

/* Admin topbar - always at the very top */
.fnx-admin-topbar {
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    flex-shrink: 0 !important;
}

/* Admin body fills remaining height exactly - no overflow/scroll needed on body */
.fnx-admin-body {
    height: calc(100vh - 64px) !important;
    overflow: hidden !important;
}

/* Sidebar scrollable */
.fnx-admin-sidebar {
    height: 100% !important;
    overflow-y: auto !important;
    flex-shrink: 0 !important;
}

/* Main content area: only this one scrolls */
.fnx-admin-main-content {
    height: 100% !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

/* Admin login page - always full screen, no scroll needed */
.fnx-admin-login-page {
    height: 100vh !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ===================================================================
   END SCROLL FIX
   =================================================================== */

"""

# Prepend the fix (after the @import line to avoid breaking import)
import_end = css.find('\n', css.find('@import'))
css_fixed = css[:import_end+1] + scroll_fix_css + css[import_end+1:]

with open(r'd:\KPMG\widget_css_patched.css', 'w', encoding='utf-8') as f:
    f.write(css_fixed)

print('CSS patched, length:', len(css_fixed))

# Now deploy BOTH patched client script AND patched CSS back to ServiceNow
r = requests.patch(
    f'{base}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f',
    auth=auth,
    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    json={
        'client_script': patched_client_script,
        'css': css_fixed
    }
)
print('PATCH status:', r.status_code)
if r.status_code in (200, 201):
    print('Widget updated successfully!')
else:
    print('ERROR:', r.text[:500])
