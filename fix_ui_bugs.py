import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
css = data['css']

# 1. CSS to hide the ServiceNow Usage Insights blue box
# We target the most common classes/attributes for the analytics icon
usage_hide_css = """
/* HIDE SERVICENOW USAGE INSIGHTS BOX GLOBALLY */
.sn-usage-insights,
.sn-analytics,
[data-original-title*="usage insights" i],
[title*="usage insights" i],
.sn-usage-tracking,
sp-usage-insights {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

/* FIX AI BUTTON OVERLAP / SHADOW ISSUES */
.fnx-admin-ai-floating-btn {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important; /* clean soft shadow, not thick offset */
    text-shadow: none !important;
    line-height: 1 !important;
    border: none !important; /* Remove the teal border that might be causing double-lines */
    background: #0B1F3A !important;
}
.fnx-admin-ai-floating-btn * {
    text-shadow: none !important;
    box-shadow: none !important;
}
.fnx-admin-ai-floating-btn::before,
.fnx-admin-ai-floating-btn::after {
    display: none !important;
}
"""

css += '\n\n' + usage_hide_css

# Deploy CSS fix
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'css': css}
)

if resp.status_code == 200:
    print("SUCCESS: UI fixes for Usage Insights and AI button deployed!")
else:
    print(f"ERROR: {resp.text[:400]}")
