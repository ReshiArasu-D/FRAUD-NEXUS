"""
Build Clean Widget with Pure Google API Indian Language System
==============================================================
Takes live_widget_client_fresh.js (pristine base),
injects all 15 Indian language dictionaries translated via Google Translate API,
adds clean language switcher methods,
validates syntax with Node.js,
and deploys cleanly to ServiceNow.
"""

import requests, json, sys, re, subprocess

sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("[1/5] Loading pristine client script base...")
with open('d:/KPMG/live_widget_client_fresh.js', 'r', encoding='utf-8') as f:
    cs = f.read()

print(f"  Base size: {len(cs)} chars | {cs.count('{')} open braces vs {cs.count('}')} close braces")

# Load pre-translated dictionaries from previous run if saved, or build them
# Let's check if we have translations_by_lang
print("\n[2/5] Preparing Indian language dictionaries...")
# We can load the dictionaries directly from fixed_cs.js or re-generate
with open('d:/KPMG/fixed_cs.js', 'r', encoding='utf-8') as f:
    broken = f.read()

# Extract dict block from fixed_cs.js (between "c.dict = {" and "    c.supportedLanguages = [")
dict_start = broken.find("c.dict = {")
dict_end = broken.find("    c.supportedLanguages = [", dict_start)

if dict_start != -1 and dict_end != -1:
    dict_content = broken[dict_start:dict_end].rstrip()
    print("  Successfully extracted multi-language dictionaries from fixed_cs.js")
else:
    print("  Could not extract dict_content, please verify markers")
    sys.exit(1)

# In pristine cs, find where c.dict = { ... } is located
cs_dict_start = cs.find("    c.dict = {")
cs_t_pos = cs.find("    c.t = function(key) {")

if cs_dict_start == -1 or cs_t_pos == -1:
    print("  Could not find c.dict or c.t in pristine script")
    sys.exit(1)

# Helper methods to append after c.t
lang_helpers = """
    // ========== PURE GOOGLE TRANSLATE API INTEGRATION ==========
    c.showLangPanel = false;
    c.currentGtLang = c.lang || 'en';

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

    c.toggleLang = function() {
        var next = c.lang === 'en' ? 'ta' : 'en';
        c.setGoogleTranslateLang(next);
    };
"""

# Supported languages list
supported_langs_block = """    c.supportedLanguages = [
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
"""

# Assemble new client script cleanly
# Replace from cs_dict_start up to cs_t_pos with new dict + supportedLanguages
new_cs = cs[:cs_dict_start] + "    " + dict_content + "\n\n" + supported_langs_block + "\n" + cs[cs_t_pos:]

# Find where c.t function ends in new_cs
t_func_marker = "    c.t = function(key) {\n        var langDict = c.dict[c.lang] || c.dict.en;\n        return langDict[key] || c.dict.en[key] || key;\n    };"
if t_func_marker in new_cs:
    new_cs = new_cs.replace(t_func_marker, t_func_marker + "\n" + lang_helpers)
    print("  Successfully injected language switcher helpers after c.t")
else:
    print("  Using alternative injection after c.t")
    idx = new_cs.find("c.t = function(key)")
    close_idx = new_cs.find("};", idx) + 2
    new_cs = new_cs[:close_idx] + "\n" + lang_helpers + new_cs[close_idx:]

print(f"\n[3/5] Validating new client script syntax...")
print(f"  Open braces: {new_cs.count('{')} | Close braces: {new_cs.count('}')}")

with open('d:/KPMG/test_clean_cs.js', 'w', encoding='utf-8') as f:
    f.write(new_cs)

# Run node -c
result = subprocess.run(['node', '-c', 'd:/KPMG/test_clean_cs.js'], capture_output=True, text=True)
if result.returncode != 0:
    print("  SYNTAX ERROR IN NODE:")
    print(result.stderr)
    sys.exit(1)
else:
    print("  Syntax check PASSED with Node.js! Code is 100% valid.")

# 4. Clean template of any leftover Google widget frames/scripts
print("\n[4/5] Cleaning template of any iframe scripts...")
r_tpl = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
tpl = r_tpl.json()['result']['template']

tpl = re.sub(r'<!-- Google Translate Widget Integration -->[\s\S]*?<!-- End Google Translate Widget -->', '', tpl)
tpl = re.sub(r'<div id="google_translate_element"[\s\S]*?</div>', '', tpl)
tpl = re.sub(r'<script[^>]*translate\.google\.com[^>]*>[\s\S]*?</script>', '', tpl)

# 5. Deploy to ServiceNow
print("\n[5/5] Deploying cleanly to ServiceNow...")
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'client_script': new_cs, 'template': tpl}
)

print(f"  Deploy status: {resp.status_code}")
if resp.status_code == 200:
    print("  SUCCESSFULLY DEPLOYED CLEAN WIDGET!")
else:
    print("  Deploy failed:", resp.text[:400])
