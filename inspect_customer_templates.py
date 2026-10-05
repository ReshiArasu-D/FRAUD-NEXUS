import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

idx1 = tpl.find("c.currentView === 'trackCases'")
print("=== trackCases template snippet (from idx %d) ===" % idx1)
print(tpl[idx1:idx1+1500])

idx2 = tpl.find("c.currentView === 'evidenceVault'")
print("\n=== evidenceVault template snippet (from idx %d) ===" % idx2)
print(tpl[idx2:idx2+1500])

idx3 = tpl.find("c.currentView === 'help'")
print("\n=== help template snippet (from idx %d) ===" % idx3)
print(tpl[idx3:idx3+1500])
