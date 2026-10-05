import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    t = f.read()

start = 164653
# Find where the next top-level admin module starts or where this div ends
next_mod = t.find("c.adminModule ===", start + 100)
end = next_mod if next_mod != -1 else start + 30000

snippet = t[start:end]
print(f"Investigation section length: {len(snippet)}")

# Print out tab definitions or headers
lines = snippet.split('\n')
for i, l in enumerate(lines):
    if 'ng-click="c.setInvestigationTab' in l or 'ng-if="c.investigationTab' in l or 'class="fnx-inv-tab' in l or 'class="fnx-btn' in l:
        print(f"L{i}: {l.strip()[:100]}")
