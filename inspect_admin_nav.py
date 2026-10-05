import re, sys

sys.stdout.reconfigure(encoding='utf-8')
with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    t = f.read()

clicks = re.findall(r'ng-click="([^"]*admin[^"]*)"', t, re.IGNORECASE)
print("Admin related ng-clicks:", set(clicks))

views = re.findall(r'c\.currentView\s*=\s*[\'"][^\'"]+[\'"]', t)
print("Views set in template:", set(views))
