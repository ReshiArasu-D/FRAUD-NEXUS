import json

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']
css = d['css']

idx = tpl.find("WELCOME BACK")
if idx == -1:
    idx = tpl.find("Welcome Back")
if idx == -1:
    idx = tpl.find("Welcome back")
if idx == -1:
    idx = tpl.find("welcome back")

print("Found welcome back at:", idx)
if idx != -1:
    print(tpl[max(0, idx-500):min(len(tpl), idx+1500)])
else:
    # search for login/register
    idx2 = tpl.find("c.authMode")
    print("Found c.authMode at:", idx2)
    if idx2 != -1:
        print(tpl[max(0, idx2-500):min(len(tpl), idx2+1500)])
