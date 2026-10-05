import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://dev187180.service-now.com/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f'
auth = ('admin', 'mn%XC1^ScdA4')
r = requests.get(url, auth=auth)
template = r.json()['result']['template']

target = '''                                <div class="fnx-field">
                                    <label>Recovered Amount (₹)</label>
                                    <input type="number" ng-model="c.reportForm.recovered_amount" placeholder="e.g. 0">
                                </div>
                            </div>
                        </div><!-- end fnx-form-grid-3 -->'''

replacement = '''                                <div class="fnx-field">
                                    <label>Recovered Amount (₹)</label>
                                    <input type="number" ng-model="c.reportForm.recovered_amount" placeholder="e.g. 0">
                                </div>
                        </div><!-- end fnx-form-grid-3 -->'''

assert target in template, 'Target not found!'
new_tpl = template.replace(target, replacement, 1)

# Now check sections in new_tpl
marks = [
    ('4A. DASHBOARD', new_tpl.find('4A. DASHBOARD VIEW')),
    ('4B. CUSTOMER PROFILE & KYC', new_tpl.find('4B. CUSTOMER PROFILE & KYC VIEW')),
    ('4C. REPORT FRAUD WIZARD', new_tpl.find('4C. REPORT FRAUD WIZARD')),
    ('4D. SUBMIT SUCCESS', new_tpl.find('4D. SUBMIT SUCCESS VIEW')),
    ('4E. TRACK CASES', new_tpl.find('4E. TRACK CASES VIEW')),
    ('4F. EVIDENCE VAULT', new_tpl.find('4F. EVIDENCE VAULT VIEW')),
    ('4G. HELP & SUPPORT', new_tpl.find('4G. HELP & SUPPORT VIEW')),
    ('END OF MAIN', new_tpl.find('</main>'))
]

for i in range(len(marks)-1):
    name, s = marks[i]
    _, e = marks[i+1]
    sec_text = new_tpl[s:e]
    tags = re.findall(r'<(div|aside|main|section)[^>]*>|</(div|aside|main|section)>', sec_text)
    depth = 0
    for open_tag, close_tag in tags:
        if open_tag:
            depth += 1
        else:
            depth -= 1
    print(f'{name} (chars {s} to {e}): net change = {depth}')

customer_main = new_tpl[new_tpl.find('<main class="fnx-content"'):new_tpl.find('</main>') + 7]
tags = re.findall(r'<(div|aside|main|section)[^>]*>|</(div|aside|main|section)>', customer_main)
stack = []
for open_tag, close_tag in tags:
    if open_tag:
        stack.append(open_tag[:30])
    else:
        if stack:
            stack.pop()
        else:
            print('EXTRA CLOSE IN CUSTOMER MAIN:', close_tag)

print('Customer main unclosed count:', len(stack))
