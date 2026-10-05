import requests, sys, re

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
data = r.json()['result']
css = data['css']

# We will append a massive block of premium CSS that targets the admin workspace classes.
# This will override the existing basic styles with high-end, modern UI styles.

premium_css = """
/* =====================================================================
   PREMIUM ADMIN UI OVERHAUL (Modern ServiceNow & Next Experience Design)
   ===================================================================== */

/* --- 1. GLOBAL ADMIN TYPOGRAPHY & BACKGROUND --- */
.fnx-admin-layout {
    background-color: #F1F5F9 !important; /* Subtle off-white for depth */
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* --- 2. HEADER / TOPBAR ENHANCEMENTS --- */
.fnx-admin-topbar {
    background: #FFFFFF !important;
    border-bottom: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    padding: 0.75rem 2rem !important;
    height: 70px !important;
}

/* Fix Logo Visibility in Header (Dark text on white background) */
.fnx-admin-topbar .fnx-brand-name {
    color: #0F172A !important;
    font-size: 1.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}
.fnx-admin-topbar .fnx-brand-tagline {
    color: #3B82F6 !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}
.fnx-admin-topbar svg path {
    fill: #EFF6FF !important;
    stroke: #2563EB !important;
}
.fnx-admin-topbar svg circle, .fnx-admin-topbar svg line {
    stroke: #2563EB !important;
}

/* --- 3. SIDEBAR REDESIGN (Premium Dark Mode) --- */
.fnx-admin-sidebar {
    background: linear-gradient(180deg, #0B1F3A 0%, #061121 100%) !important;
    border-right: 1px solid #1E293B !important;
    box-shadow: 4px 0 15px rgba(0,0,0,0.1) !important;
}
.fnx-sidebar-item {
    border-radius: 8px !important;
    margin: 0.2rem 1rem !important;
    padding: 0.85rem 1rem !important;
    color: #94A3B8 !important;
    transition: all 0.2s ease !important;
}
.fnx-sidebar-item:hover {
    background: rgba(255,255,255,0.05) !important;
    color: #FFFFFF !important;
}
.fnx-sidebar-item.active {
    background: rgba(37, 99, 235, 0.15) !important;
    color: #60A5FA !important;
    border-left: 4px solid #3B82F6 !important;
}
.fnx-sidebar-item.active .fnx-sidebar-icon svg {
    stroke: #60A5FA !important;
}

/* --- 4. MODERN CARD STYLING (KPIs & Widgets) --- */
.fnx-kpi-card, .fnx-card, .fnx-cc-card {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
.fnx-kpi-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04) !important;
}

/* --- 5. PREMIUM DATA TABLES --- */
/* Target all main tables in the admin dashboard */
.fnx-table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: 100% !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02) !important;
    background: #FFFFFF !important;
}
.fnx-table thead {
    background-color: #F8FAFC !important;
}
.fnx-table th {
    padding: 1rem 1.25rem !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #475569 !important;
    border-bottom: 2px solid #E2E8F0 !important;
}
.fnx-table td {
    padding: 1rem 1.25rem !important;
    font-size: 0.875rem !important;
    color: #1E293B !important;
    border-bottom: 1px solid #F1F5F9 !important;
    vertical-align: middle !important;
}
.fnx-table tbody tr {
    transition: background-color 0.2s ease !important;
}
.fnx-table tbody tr:hover {
    background-color: #F8FAFC !important;
}
.fnx-table tbody tr:last-child td {
    border-bottom: none !important;
}

/* --- 6. MODERN BUTTONS --- */
.fnx-btn {
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}
.fnx-btn-primary {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    border: none !important;
    color: white !important;
}
.fnx-btn-primary:hover {
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    transform: translateY(-1px) !important;
}
.fnx-btn-outline {
    border: 1px solid #CBD5E1 !important;
    color: #334155 !important;
    background: #FFFFFF !important;
}
.fnx-btn-outline:hover {
    background: #F8FAFC !important;
    border-color: #94A3B8 !important;
}

/* --- 7. STATUS PILLS & BADGES --- */
.fnx-status-pill, .fnx-badge, .fnx-risk-pill {
    padding: 0.25rem 0.75rem !important;
    border-radius: 9999px !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}
/* Default subtle badge */
.fnx-status-pill {
    background: #F1F5F9 !important;
    color: #475569 !important;
}
/* High Risk / Critical */
.fnx-risk-pill.risk-high, .sev-critical {
    background: #FEF2F2 !important;
    color: #DC2626 !important;
    border: 1px solid #FCA5A5 !important;
}
/* Medium Risk */
.sev-medium {
    background: #FFFBEB !important;
    color: #D97706 !important;
    border: 1px solid #FCD34D !important;
}

/* --- 8. SEARCH BAR MODERNIZATION --- */
.fnx-search-input, input[type="search"] {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.9rem !important;
    color: #1E293B !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) inset !important;
    transition: all 0.2s ease !important;
}
.fnx-search-input:focus, input[type="search"]:focus {
    outline: none !important;
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
}

/* --- 9. TAB NAVIGATION MODERNIZE --- */
.fnx-tabs {
    border-bottom: 2px solid #E2E8F0 !important;
    display: flex !important;
    gap: 2rem !important;
    margin-bottom: 1.5rem !important;
}
.fnx-tab {
    padding: 0.75rem 0 !important;
    font-weight: 600 !important;
    color: #64748B !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.fnx-tab:hover {
    color: #0F172A !important;
}
.fnx-tab.active {
    color: #2563EB !important;
    border-bottom: 2px solid #2563EB !important;
}
"""

css += '\n\n' + premium_css

# Push updates
print("Deploying premium CSS...")
resp = requests.patch(
    f"{base}/api/now/table/sp_widget/{WIDGET_ID}",
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json={'css': css}
)

if resp.status_code == 200:
    print("SUCCESS: Premium UI styling deployed!")
else:
    print(f"ERROR: {resp.text[:400]}")
