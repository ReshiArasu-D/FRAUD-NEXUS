import requests, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

print("Fetching latest live widget from ServiceNow...")
r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
if r.status_code != 200:
    print('Failed to fetch widget:', r.text)
    sys.exit(1)

w = r.json()['result']
template = w['template']
client = w['client_script']
css = w['css']
server = w.get('script', '')

print(f"Fetched successfully! Template: {len(template)} bytes, Client: {len(client)} bytes, CSS: {len(css)} bytes, Server: {len(server)} bytes.")

# Write to canonical files
with open('d:/KPMG/widget_template.html', 'w', encoding='utf-8') as f:
    f.write(template)
print("Updated d:/KPMG/widget_template.html")

with open('d:/KPMG/widget_style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated d:/KPMG/widget_style.css")

with open('d:/KPMG/test_widget_client.js', 'w', encoding='utf-8') as f:
    f.write(client)
print("Updated d:/KPMG/test_widget_client.js")

with open('d:/KPMG/widget_client.js', 'w', encoding='utf-8') as f:
    f.write(client)
print("Updated d:/KPMG/widget_client.js")

with open('d:/KPMG/widget_server.js', 'w', encoding='utf-8') as f:
    f.write(server)
print("Updated d:/KPMG/widget_server.js")

