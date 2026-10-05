import requests, json

WIDGET_SYS_ID = '2f258577c32b43d0e54832f1b401317f'
BASE_URL = 'https://dev187180.service-now.com'
AUTH = ('admin', 'mn%XC1^ScdA4')

r = requests.get(f'{BASE_URL}/api/now/table/sp_widget/{WIDGET_SYS_ID}', auth=AUTH)
template = r.json()['result']['template']

pos = template.find('Recent Cases')
tbody_pos = template.find('<tbody>', pos)
tbody_end = template.find('</tbody>', tbody_pos)
print(template[tbody_pos:tbody_end+8])

