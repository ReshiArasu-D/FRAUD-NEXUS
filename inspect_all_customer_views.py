import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

idx_track = tpl.find("c.currentView === 'trackCases'")
# find the next view
idx_ev = tpl.find("c.currentView === 'evidenceVault'", idx_track + 100)
idx_help = tpl.find("c.currentView === 'help'", idx_ev + 100)
idx_end = tpl.find("c.showAI", idx_help)

print("=== TRACK CASES (len %d) ===" % (idx_ev - idx_track))
print(tpl[idx_track:idx_ev])

print("\n=== EVIDENCE VAULT (len %d) ===" % (idx_help - idx_ev))
print(tpl[idx_ev:idx_help])

print("\n=== HELP VIEW (len %d) ===" % (idx_end - idx_help))
print(tpl[idx_help:idx_end])
