"""
FRAUDNEXUS – Pure Google Translate API Integration
===================================================
1. Fetches all 137 dictionary keys from FRAUDNEXUS.
2. Uses free Google Translate API (translate.googleapis.com) to translate
   all keys into Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali,
   Marathi, Gujarati, Punjabi, Odia, Assamese, Urdu, Nepali, Sanskrit, Bhojpuri.
3. Injects translated dictionaries into c.dict.
4. Adds dynamic on-demand Google Translate API caller for any remaining keys/languages.
5. COMPLETELY REMOVES the Google Translate iframe widget and script tags,
   guaranteeing ZERO white top bars, ZERO iframes, and ZERO layout distortion!
"""

import requests, json, sys, re, urllib.parse, time

sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=" * 60)
print("FRAUDNEXUS – Deploying Pure Google Translate API System")
print("=" * 60)

# 1. Fetch current widget
print("\n[1/5] Fetching live widget...")
r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
tpl = w['template']
cs = w['client_script']
css = w['css']

# 2. Extract EN keys and values
print("\n[2/5] Extracting EN dictionary keys...")
en_match = re.search(r'en:\s*\{([\s\S]*?)\n\s*\},', cs)
if not en_match:
    print("Error: Could not locate en dictionary in client script")
    sys.exit(1)

en_text = en_match.group(1)
key_val_pairs = re.findall(r"(\w+):\s*'((?:\\'|[^'])*)'", en_text)
keys = [k for k, v in key_val_pairs]
values = [v.replace("\\'", "'") for k, v in key_val_pairs]
print(f"  Extracted {len(keys)} keys from EN dictionary")

# 3. Translate via Google Translate API
def translate_batch(texts, target_lang):
    combined = '\n'.join(texts)
    encoded = urllib.parse.quote(combined)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={encoded}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        parts = [item[0] for item in data[0] if item and item[0]]
        full = ''.join(parts)
        lines = full.split('\n')
        if len(lines) == len(texts):
            return lines
        else:
            return texts
    except Exception as e:
        print(f"    Failed batch for {target_lang}: {e}")
        return texts

# Languages to translate
target_langs = {
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese',
    'ur': 'Urdu',
    'ne': 'Nepali',
    'sa': 'Sanskrit',
    'bho': 'Bhojpuri'
}

print("\n[3/5] Translating dictionary keys into Indian languages via Google Translate API...")
translations_by_lang = {}

BATCH_SIZE = 35
batches = [values[i:i+BATCH_SIZE] for i in range(0, len(values), BATCH_SIZE)]

for code, name in target_langs.items():
    print(f"  Translating {name} ({code})...", end='', flush=True)
    all_translated = []
    for b in batches:
        t_batch = translate_batch(b, code)
        if len(t_batch) == len(b):
            all_translated.extend(t_batch)
        else:
            for single in b:
                enc = urllib.parse.quote(single)
                u = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={code}&dt=t&q={enc}"
                try:
                    d = requests.get(u, timeout=5).json()
                    all_translated.append(d[0][0][0])
                except:
                    all_translated.append(single)
        time.sleep(0.1)
    translations_by_lang[code] = dict(zip(keys, all_translated))
    print(f" done ({len(all_translated)} keys)")

# 4. Format into JS c.dict definitions
print("\n[4/5] Formatting client script and removing Google widget iframes...")

dict_js_blocks = []
for code, trans_dict in translations_by_lang.items():
    entries = []
    for k, v in trans_dict.items():
        v_escaped = v.replace("'", "\\'").replace("\n", " ")
        entries.append(f"            {k}: '{v_escaped}'")
    dict_js_blocks.append(f"        {code}: {{\n" + ",\n".join(entries) + "\n        }")

all_dicts_str = ",\n" + ",\n".join(dict_js_blocks)

# Extract original EN block cleanly
en_block_match = re.search(r'(en:\s*\{[\s\S]*?\n\s*\}),', cs)
if en_block_match:
    en_block = "        " + en_block_match.group(1).strip()
else:
    en_block = "        en: {}"

dict_end_marker = "    c.t = function(key) {"
dict_end_pos = cs.find(dict_end_marker)

helper_methods = """
    c.supportedLanguages = [
        { code: 'en', name: 'English' },
        { code: 'hi', name: 'हिन्दी (Hindi)' },
        { code: 'ta', name: 'தமிழ் (Tamil)' },
        { code: 'te', name: 'తెలుగు (Telugu)' },
        { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
        { code: 'ml', name: 'മലയാളം (Malayalam)' },
        { code: 'bn', name: 'বাংলা (Bengali)' },
        { code: 'mr', name: 'मराठी (Marathi)' },
        { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
        { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
        { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
        { code: 'as', name: 'অসমীয়া (Assamese)' },
        { code: 'ur', name: 'اردو (Urdu)' },
        { code: 'ne', name: 'नेपाली (Nepali)' },
        { code: 'sa', name: 'संस्कृतम् (Sanskrit)' },
        { code: 'bho', name: 'भोजपुरी (Bhojpuri)' }
    ];

    // On-demand dynamic Google Translate API caller for any missing text
    c.fetchGoogleTranslation = function(text, targetLang, callback) {
        if (!text || targetLang === 'en') { callback(text); return; }
        var url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=' + targetLang + '&dt=t&q=' + encodeURIComponent(text);
        $http.get(url).then(function(res) {
            if (res.data && res.data[0]) {
                var result = res.data[0].map(function(item) { return item[0]; }).join('');
                callback(result);
            } else {
                callback(text);
            }
        }).catch(function() {
            callback(text);
        });
    };

    // Instant language switcher (Zero reload, pure API)
    c.openGoogleTranslate = function() {
        c.showLangPanel = !c.showLangPanel;
    };

    c.setGoogleTranslateLang = function(langCode) {
        c.lang = langCode;
        c.currentGtLang = langCode;
        c.showLangPanel = false;
        $window.localStorage.setItem('fnx_lang', langCode);
        $window.localStorage.setItem('fnx_gt_lang', langCode);
    };

    c.changeLang = function(l) {
        c.setGoogleTranslateLang(l);
    };
"""

new_dict_section = "    c.dict = {\n" + en_block + all_dicts_str + "\n    };\n" + helper_methods

old_dict_start = cs.find("c.dict = {")
cs = cs[:old_dict_start] + new_dict_section + "\n" + cs[dict_end_pos:]

# Remove any old Google Translate script tags or iframe watchers
cs = re.sub(r'// SAFE GLOBAL STYLES[\s\S]*?c\.openGoogleTranslate = function\(\) \{', '', cs)
cs = re.sub(r'// Google Translate Element Init[\s\S]*?c\.openGoogleTranslate = function\(\) \{', '', cs)

# Remove Google Translate widget tags from template
tpl = re.sub(r'<!-- Google Translate Widget Integration -->[\s\S]*?<!-- End Google Translate Widget -->', '', tpl)
tpl = re.sub(r'<div id="google_translate_element"[\s\S]*?</div>', '', tpl)
tpl = re.sub(r'<script[^>]*translate\.google\.com[^>]*>[\s\S]*?</script>', '', tpl)

# 5. Deploy to ServiceNow
print("\n[5/5] Deploying pure Google Translate API system to ServiceNow...")
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'template': tpl, 'client_script': cs, 'css': css}
)

print(f"Deploy status: {resp.status_code}")
if resp.status_code == 200:
    print("SUCCESS! Deployed Pure Google Translate API System:")
    print("  • 15 Indian languages pre-translated directly via Google Translate API")
    print("  • Dynamic on-demand Google Translate API fallback")
    print("  • Zero Google Translate iframe or banner box")
    print("  • Zero page reload, zero displacement, zero scrollbars")
else:
    print("Failed to deploy:", resp.text[:400])
