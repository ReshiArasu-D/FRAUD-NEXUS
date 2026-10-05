import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

idx_track = 94090
idx_ev = 98664
idx_help = 103925
idx_end = 106603

print("=== TRACK CASES (from %d to %d) ===" % (idx_track, idx_ev))
print(tpl[idx_track:idx_ev])

print("\n=== EVIDENCE VAULT (from %d to %d) ===" % (idx_ev, idx_help))
print(tpl[idx_ev:idx_help])

print("\n=== HELP VIEW (from %d to %d) ===" % (idx_help, idx_end))
print(tpl[idx_help:idx_end])
