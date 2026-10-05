import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    t = f.read()

inv_start_marker = "c.adminModule === 'investigation'\" class=\"fnx-investigation-workspace\""
inv_start = t.find(inv_start_marker)
div_start = t.rfind("<div", 0, inv_start)

# Find where partners starts
part_start = t.find("c.adminModule === 'partners'", inv_start + 100)
div_end = t.rfind("</div>", 0, part_start)

print("Investigation div start:", div_start)
print("Partners starts at:", part_start)
print("Div end before partners:", div_end)

print("--- Header before div_start ---")
print(t[div_start-100:div_start])
print("--- End after div_end ---")
print(t[div_end:div_end+200])
