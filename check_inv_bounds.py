import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    t = f.read()

start_marker = "c.adminModule === 'investigation'\" class=\"fnx-investigation-workspace\""
start = t.find(start_marker)
print("Start marker at:", start)
if start != -1:
    # Find start of div
    div_start = t.rfind("<div", 0, start)
    print("Div start at:", div_start)
    
    # Find next module or closing div
    next_mod = t.find("c.adminModule === 'intelligence'", start)
    print("Next module at:", next_mod)
    div_end = t.rfind("</div>", 0, next_mod)
    print("Div end at:", div_end)
    
    print("\nText leading up to div_end:")
    print(t[div_end-100:div_end+200])
