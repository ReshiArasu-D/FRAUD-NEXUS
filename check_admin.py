with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()
idx = tpl.find("class=\"fnx-admin-layout\"")
print(tpl[max(0, idx):idx+1200])
