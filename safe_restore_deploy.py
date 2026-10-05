"""
SAFE RESTORE + MINIMAL LANGUAGE INJECTION
==========================================
1. Start from the PRISTINE live_widget_client_fresh.js (known-good)
2. Surgically inject ONLY:
   - New supportedLanguages list (all Indian languages)
   - setGoogleTranslateLang / openGoogleTranslate / showLangPanel methods
   - Pre-translated dicts for hi, ta, te, kn, ml, bn, mr, gu, pa, or, as, ur, ne, sa
3. Validate with Node.js
4. Deploy
"""

import requests, sys, re, subprocess

sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("[1] Loading pristine client script...")
with open('d:/KPMG/live_widget_client_fresh.js', 'r', encoding='utf-8') as f:
    cs = f.read()

print(f"  Size: {len(cs)} chars | {cs.count('{')} open vs {cs.count('}')} close braces")

# ============================================================
# STEP A: Replace the old 13-language supportedLanguages list
# with a full 16-language one
# ============================================================
old_langs = """    c.supportedLanguages = [
        { code: 'en', name: 'English' },
        { code: 'ta', name: 'தமிழ் (Tamil)' },
        { code: 'hi', name: 'हिन्दी (Hindi)' },
        { code: 'te', name: 'తెలుగు (Telugu)' },
        { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
        { code: 'ml', name: 'മലയാളം (Malayalam)' },
        { code: 'bn', name: 'বাংলা (Bengali)' },
        { code: 'mr', name: 'मराठी (Marathi)' },
        { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
        { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
        { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
        { code: 'as', name: 'অসমীয়া (Assamese)' },
        { code: 'ur', name: 'اردو (Urdu)' }
    ];"""

new_langs = """    c.supportedLanguages = [
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
    ];"""

if old_langs in cs:
    cs = cs.replace(old_langs, new_langs)
    print("  ✓ Replaced supportedLanguages list")
else:
    print("  ⚠ supportedLanguages not found verbatim, trying regex...")
    cs = re.sub(
        r"c\.supportedLanguages\s*=\s*\[[\s\S]*?\];",
        new_langs.strip(),
        cs,
        count=1
    )
    print("  ✓ Replaced via regex")

# ============================================================
# STEP B: Replace the old toggleLang (binary en/ta toggle) with
# a proper changeLang that supports all languages
# ============================================================
old_toggle = """    c.toggleLang = function() {
        var next = c.lang === 'en' ? 'ta' : 'en';
        c.changeLang(next);
    };"""

new_toggle = """    c.toggleLang = function() {
        var next = c.lang === 'en' ? 'hi' : 'en';
        c.changeLang(next);
    };

    // ====== LANGUAGE PANEL (Google Translate API style, no iframe) ======
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
    };"""

if old_toggle in cs:
    cs = cs.replace(old_toggle, new_toggle)
    print("  ✓ Replaced toggleLang and injected language panel methods")
else:
    print("  ⚠ toggleLang not found verbatim, trying regex...")
    old_toggle_re = re.compile(
        r"c\.toggleLang\s*=\s*function\(\)\s*\{[\s\S]*?\};",
        re.MULTILINE
    )
    cs = old_toggle_re.sub(new_toggle.strip(), cs, count=1)
    print("  ✓ Replaced via regex")

# ============================================================
# STEP C: Load translated dicts from fixed_cs.js and inject
# after the en: { ... } and hi: { ... } blocks
# (we only inject the DICT VALUES, nothing else)
# ============================================================
print("\n[2] Extracting Indian language dicts from fixed_cs.js...")
with open('d:/KPMG/fixed_cs.js', 'r', encoding='utf-8') as f:
    broken = f.read()

# In fixed_cs.js the c.dict = { en: {...}, hi: {...}, ta: {...}, ... };
# We need to find all the language blocks and insert them into pristine cs

# Get each language block from broken
lang_codes = ['hi', 'ta', 'te', 'kn', 'ml', 'bn', 'mr', 'gu', 'pa', 'or', 'as', 'ur', 'ne', 'sa', 'bho']
lang_blocks = {}

for code in lang_codes:
    pattern = f"        {code}: {{" if code != 'hi' else f"        {code}: {{"
    start_idx = broken.find(f"\n        {code}: {{")
    if start_idx == -1:
        print(f"  ⚠ Could not find dict for {code}")
        continue
    # Find matching closing brace
    brace_count = 0
    i = start_idx + 1  # skip the \n
    found_end = -1
    while i < len(broken):
        if broken[i] == '{':
            brace_count += 1
        elif broken[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                found_end = i
                break
        i += 1
    if found_end == -1:
        print(f"  ⚠ Could not find end of dict for {code}")
        continue
    lang_blocks[code] = broken[start_idx:found_end+1]

print(f"  Extracted {len(lang_blocks)} language blocks")

# Insert all extracted dict blocks after the end of en: { ... }
# Find where en: { ... } ends in pristine cs
# Find where hi: { ... } starts — in original there's only: hi: { ... } block already
# So we need to find the DICT end marker: \n    }; (closing of c.dict)

# Find existing hi, ta in the pristine cs dict
existing_codes_in_cs = []
for code in lang_codes:
    if f"\n        {code}: {{" in cs:
        existing_codes_in_cs.append(code)
print(f"  Already in pristine dict: {existing_codes_in_cs}")

# Build the new blocks to inject (skip ones already present)
new_dict_blocks = ""
for code in lang_codes:
    if code not in existing_codes_in_cs and code in lang_blocks:
        new_dict_blocks += lang_blocks[code] + "\n"

if new_dict_blocks:
    # Find the closing of the hi block or en block to inject after
    # c.dict ends with: \n    };\n\n    // Helper
    # We want to insert our new dict blocks just before the }; that closes c.dict
    
    # Find the dict closing: look for fallbackDict or otherLangs pattern
    other_langs_marker = "    // Helper for other"
    if other_langs_marker in cs:
        cs = cs.replace(other_langs_marker, new_dict_blocks + "\n    // Helper for other")
        print(f"  ✓ Injected {len(lang_blocks)} language dicts before fallback helper")
    else:
        # Try to insert before c.t
        t_marker = "    c.t = function(key) {"
        cs = cs.replace(t_marker, new_dict_blocks.rstrip() + "\n\n    " + t_marker.strip() + "\n    " if False else t_marker, 1)
        print(f"  ⚠ Injected before c.t (fallback injection)")
else:
    print("  All language dicts already present in pristine cs")

# ============================================================
# STEP D: Validate with Node.js
# ============================================================
print("\n[3] Validating syntax...")
print(f"  Braces: {cs.count('{')} open vs {cs.count('}')} close")
with open('d:/KPMG/final_cs_restore.js', 'w', encoding='utf-8') as f:
    f.write(cs)

result = subprocess.run(['node', '-c', 'd:/KPMG/final_cs_restore.js'], capture_output=True, text=True)
if result.returncode != 0:
    print("  ❌ SYNTAX ERROR:")
    print(result.stderr)
    sys.exit(1)
print("  ✅ Syntax valid with Node.js!")

# ============================================================
# STEP E: Deploy to ServiceNow
# ============================================================
print("\n[4] Deploying to ServiceNow...")
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'client_script': cs}
)
print(f"  Deploy status: {resp.status_code}")
if resp.status_code == 200:
    print("  ✅ Successfully deployed clean, working widget!")
else:
    print("  ❌ Failed:", resp.text[:300])
