import requests, json

# Check the live page via CDP or check the widget
WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
w = r.json()['result']
template = w['template']

# Let's inspect the entire section between trackCases and help
idx_track = template.find("c.currentView === 'trackCases'")
idx_ev = template.find("c.currentView === 'evidenceVault'")
idx_edit = template.find("c.currentView === 'editProfile'")
idx_help = template.find("c.currentView === 'help'")

print(f"Indices in template:\nTrack: {idx_track}\nEvidenceVault: {idx_ev}\nEditProfile: {idx_edit}\nHelp: {idx_help}")

# Check around each of these tags:
print("\n--- AROUND EVIDENCE VAULT ---")
print(template[idx_ev-60:idx_ev+250])

print("\n--- AROUND EDIT PROFILE ---")
print(template[idx_edit-60:idx_edit+250])

print("\n--- AROUND HELP ---")
print(template[idx_help-60:idx_help+250])

