import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("HTML length:", len(html))

# Find adminWorkspace block
adm_start = html.find("c.currentView === 'adminWorkspace'")
if adm_start != -1:
    adm_html = html[adm_start:]
    print("Found adminWorkspace block at index", adm_start, "length:", len(adm_html))
    
    # Print sub-headings, nav items, buttons, tabs
    nav_matches = re.findall(r'<li[^>]*>.*?</li>|<button[^>]*>.*?</button>|<a[^>]*>.*?</a>', adm_html[:5000], re.DOTALL)
    print("\n--- First few interactive elements in adminWorkspace ---")
    for el in nav_matches[:25]:
        clean = " ".join(el.split())
        print(" ", clean[:100])
        
    # Check for tab structures or sub-views in admin workspace
    print("\n--- Directives in admin workspace ---")
    ng_ifs = re.findall(r'ng-if="([^"]+)"', adm_html)
    print("Unique ng-if conditions:", set(ng_ifs))
    
    ng_clicks = re.findall(r'ng-click="([^"]+)"', adm_html)
    print("Sample ng-clicks:", set(list(ng_clicks)[:30]))
else:
    print("adminWorkspace not found in current_deployed_template.html!")
