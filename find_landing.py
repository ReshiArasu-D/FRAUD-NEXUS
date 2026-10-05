with open('d:/KPMG/working_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

idx = tpl.find("c.currentView === 'landing'")
print(tpl[max(0, idx-100):idx+500])
