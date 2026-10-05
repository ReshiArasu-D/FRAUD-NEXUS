import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    t = f.read()

start = t.find("c.adminModule === 'investigation'")
if start != -1:
    print("Found investigation section at index", start)
    # find next c.adminModule
    next_mod = t.find("c.adminModule ===", start + 50)
    end = next_mod if next_mod != -1 else start + 25000
    section_html = t[start:end]
    print(f"Investigation HTML length: {len(section_html)}")
    print(section_html[:3000])
else:
    print("investigation module not found!")
