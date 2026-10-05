import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'

# Get current widget
r = requests.get(f'{base}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
cs = w.get('client_script', '')

# Find the Tamil addTask entry
ta_marker = "addTask: '\u0baa\u0ba3\u0bbf \u0b9a\u0bc7\u0bb0\u0bcd\u0b95\u0bcd\u0b95',"
print('TA addTask found:', ta_marker in cs)

# Alternative: find Tamil commandCenter
ta_cmd = "\u0b95\u0b9f\u0bcd\u0b9f\u0bb3\u0bc8 \u0bae\u0bc8\u0baf\u0bae\u0bcd"
print('TA commandCenter phrase found:', ta_cmd in cs)

ta_insert = """            partners: '\u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd\u0b95\u0bb3\u0bcd',
            partnerDirectory: '\u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd \u0b85\u0b9f\u0bc8\u0bb5\u0bc1',
            addPartner: '\u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd \u0b9a\u0bc7\u0bb0\u0bcd\u0b95\u0bcd\u0b95',
            editPartner: '\u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd \u0ba4\u0bbf\u0bb0\u0bc1\u0ba4\u0bcd\u0ba4\u0bc1',
            partnerRequests: '\u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd \u0b95\u0bcb\u0bb0\u0bbf\u0b95\u0bcd\u0b95\u0bc8\u0b95\u0bb3\u0bcd',
            requestStatus: '\u0b95\u0bcb\u0bb0\u0bbf\u0b95\u0bcd\u0b95\u0bc8 \u0ba8\u0bbf\u0bb2\u0bc8',
            partnerCategory: '\u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd \u0bb5\u0b95\u0bc8',
            integrationType: '\u0b87\u0ba3\u0bc8\u0baa\u0bcd\u0baa\u0bc1 \u0bb5\u0b95\u0bc8',
            simulatedDemoPartner: '\u0baa\u0bcb\u0bb2\u0bbf \u0bae\u0bbe\u0ba4\u0bbf\u0bb0\u0bbf \u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd',
            totalPartners: '\u0bae\u0bca\u0ba4\u0bcd\u0ba4 \u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd\u0b95\u0bb3\u0bcd',
            activePartners: '\u0b9a\u0bc6\u0baf\u0bb2\u0bbf\u0bb2\u0bcd \u0b89\u0bb3\u0bcd\u0bb3 \u0b95\u0bc2\u0b9f\u0bcd\u0b9f\u0bbe\u0bb3\u0bb0\u0bcd\u0b95\u0bb3\u0bcd',"""

# Strategy: inject after 'addTask' of the commandCenter translations (EN)
# The structure is: en: { ... }, ta: { ... }
# Find start of TA section
ta_section_marker = "commandCenter: '\u0b95\u0b9f\u0bcd\u0b9f\u0bb3\u0bc8 \u0bae\u0bc8\u0baf\u0bae\u0bcd',"
print('TA commandCenter marker found:', ta_section_marker in cs)

# If marker found, the TA already has commandCenter - the issue is Tamil addTask was added after
# Let's look for the TA section logout or settings key
ta_logout_orig = "logout: '\u0bb2\u0bcb\u0b95\u0bcd \u0b85\u0bb5\u0bc1\u0b9f\u0bcd',"
print('TA logout found:', ta_logout_orig in cs)

if ta_logout_orig in cs:
    # Insert partner translations after the TA logout
    insert_after = ta_logout_orig
    new_content = ta_logout_orig + "\n" + ta_insert
    cs_patched = cs.replace(insert_after, new_content)
    print('Patching...', 'partners:' in cs_patched)
    
    # Deploy
    payload = {'client_script': cs_patched}
    resp = requests.patch(
        f'{base}/api/now/table/sp_widget/2f258577c32b43d0e54832f1b401317f',
        auth=auth,
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        json=payload
    )
    print('Deploy status:', resp.status_code)
else:
    print('ERROR: Could not find TA logout marker. Trying fallback...')
    # Find TA commandCenter 
    idx_ta_cmd = cs.find(ta_section_marker)
    if idx_ta_cmd > 0:
        print('Found TA commandCenter at:', idx_ta_cmd)
        # Find the closing of TA section
        closing_markers = ["        },\n        ta: {", "    };\n    c.lang"]
        for cm in closing_markers:
            cidx = cs.find(cm, idx_ta_cmd)
            if cidx > 0:
                print('Found closing marker at:', cidx, '|->', cs[cidx:cidx+50])
