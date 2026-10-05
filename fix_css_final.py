import requests, sys, re

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
css = data['css']

# 1. Clean up old `.fnx-btn-demo` CSS rules
css = re.sub(r'\.fnx-btn-demo\s*\{[^}]*\}', '', css)
css = re.sub(r'\.fnx-btn-demo:hover\s*\{[^}]*\}', '', css)
css = re.sub(r'\.fnx-btn-demo,\s*button\[type="submit"\]\s*\{[^}]*\}', 'button[type="submit"] { width: 100% !important; padding: 0.9rem !important; font-weight: 600 !important; font-size: 0.95rem !important; border-radius: 8px !important; margin-top: 1rem !important; cursor: pointer !important; transition: all 0.3s ease !important; text-align: center !important; }', css)

# 2. Clean up old `.fnx-admin-ai-floating-btn` CSS rules
css = re.sub(r'\.fnx-admin-ai-floating-btn\s*\{[^}]*\}', '', css)
css = re.sub(r'\.fnx-admin-ai-floating-btn:hover\s*\{[^}]*\}', '', css)
css = re.sub(r'\.fnx-admin-ai-floating-btn\s*\*\s*\{[^}]*\}', '', css)
css = re.sub(r'\.fnx-admin-ai-floating-btn::before,\s*\.fnx-admin-ai-floating-btn::after\s*\{[^}]*\}', '', css)

# 3. Add fresh, aggressive CSS fixes
new_css = """
/* =========================================
   UI FIXES: DEMO BUTTON, AI BUTTON, VA, LAYOUT
   ========================================= */

/* 1. AGGRESSIVELY HIDE VIRTUAL AGENT & USAGE INSIGHTS */
.sn-usage-insights,
.sn-analytics,
[data-original-title*="usage insights" i],
[title*="usage insights" i],
.sn-usage-tracking,
sp-usage-insights,
.sn-va-widget-icon,
#sn-va-web-client-app,
.sn-connect-fab,
div[sn-waterfall="true"],
.help-button-container {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    z-index: -9999 !important;
    width: 0 !important;
    height: 0 !important;
}

/* 2. DEMO BUTTON (Clear Text & Color) */
.fnx-btn-demo {
    width: 100% !important;
    padding: 1rem 1.5rem !important;
    background-color: #EFF6FF !important;
    background-image: none !important;
    border: 2px solid #93C5FD !important;
    border-radius: 8px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease-in-out !important;
    color: #1E3A8A !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    text-shadow: none !important;
    box-shadow: none !important;
}

.fnx-btn-demo:hover {
    background-color: #DBEAFE !important;
    border-color: #3B82F6 !important;
    color: #1E3A8A !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
}

.fnx-btn-demo .fnx-demo-badge {
    background: #1E3A8A !important;
    color: #FFFFFF !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 0.7rem !important;
}

/* 3. AI BUTTON (No shadow overlap, no pseudo elements) */
.fnx-admin-ai-floating-btn {
    position: fixed !important;
    bottom: 24px !important;
    right: 28px !important;
    background-color: #0B1F3A !important;
    background-image: none !important;
    color: #FFFFFF !important;
    border: none !important; 
    outline: none !important;
    padding: 0.8rem 1.5rem !important;
    border-radius: 30px !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    z-index: 99999 !important;
    line-height: 1.2 !important;
    text-shadow: none !important;
}

.fnx-admin-ai-floating-btn:hover {
    background-color: #123B63 !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
}

.fnx-admin-ai-floating-btn * {
    text-shadow: none !important;
    box-shadow: none !important;
    border: none !important;
}

/* Kill any pseudo-elements completely */
.fnx-admin-ai-floating-btn::before,
.fnx-admin-ai-floating-btn::after {
    display: none !important;
    content: '' !important;
    opacity: 0 !important;
}

/* 4. ADMIN DASHBOARD LAYOUT & SCROLL FIX */
/* ServiceNow adds padding to .sp-widget-content. We must force it to fill screen */
.sp-page-root section.page, .sp-page-root main {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}

.sp-widget-content {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}

.fnx-admin-page-view, .fnx-command-center {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow-y: auto !important; /* Only inner content scrolls */
    overflow-x: hidden !important;
    padding: 2rem !important;
    box-sizing: border-box !important;
}
"""

css += '\n\n' + new_css

resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'css': css}
)

if resp.status_code == 200:
    print("SUCCESS: Full CSS cleanup and layout fixes deployed!")
else:
    print(f"ERROR: {resp.text[:400]}")
