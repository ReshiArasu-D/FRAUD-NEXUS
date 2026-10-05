import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

modules = re.findall(r"setAdminModule\('([^']+)'\)", tpl)
print('Admin modules in template:', list(set(modules)))

checks = [
    ('Partners sidebar item', "partners"),
    ('Partners workspace view', "adminModule === 'partners'"),
    ('Partner directory table', "fnx-partner-directory"),
    ('Add partner modal/form', "addPartner"),
    ('Partner KPI cards', "partnerStats"),
    ('Back btn admin login -> portalSelect', "'portalSelect'"),
    ('Back btn customer login', "fnx-auth-back"),
    ('Back btn registration', "fnx-reg-back"),
]

for name, keyword in checks:
    found = keyword in tpl
    status = 'DONE' if found else 'MISSING'
    print(f'[{status}] {name}')
