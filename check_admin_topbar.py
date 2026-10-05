with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()
idx = tpl.find("class=\"fnx-admin-layout\"")
idx2 = tpl.find("</header>", idx)
print(tpl[max(0, idx2-50):idx2+800])
