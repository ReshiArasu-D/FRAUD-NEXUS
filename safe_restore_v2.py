"""
SAFE RESTORE + MINIMAL LANGUAGE INJECTION - FIXED
===================================================
Correctly inserts all language dicts INSIDE c.dict = { ... }
before its closing brace.
"""

import requests, sys, re, subprocess

sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("[1] Loading pristine client script...")
with open('d:/KPMG/live_widget_client_fresh.js', 'r', encoding='utf-8') as f:
    cs = f.read()

print(f"  Size: {len(cs)} | {cs.count('{')} open vs {cs.count('}')} close braces")

# ============================================================
# STEP A: Expand supportedLanguages to all Indian languages
# ============================================================
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

cs = re.sub(
    r"c\.supportedLanguages\s*=\s*\[[\s\S]*?\];",
    new_langs.strip(),
    cs,
    count=1
)
print("  ✓ Updated supportedLanguages")

# ============================================================
# STEP B: Add openGoogleTranslate + setGoogleTranslateLang
#         after toggleLang
# ============================================================
toggle_pat = re.compile(
    r"(c\.toggleLang\s*=\s*function\(\)\s*\{[\s\S]*?\};)",
    re.MULTILINE
)
gt_methods = """

    // ====== LANGUAGE PANEL ======
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

cs = toggle_pat.sub(lambda m: m.group(1) + gt_methods, cs, count=1)
print("  ✓ Injected openGoogleTranslate + setGoogleTranslateLang after toggleLang")

# ============================================================
# STEP C: Inject extra lang dicts INSIDE c.dict = { ... }
#         just before the helper comment line
# ============================================================
print("\n[2] Extracting language dicts from fixed_cs.js...")
with open('d:/KPMG/fixed_cs.js', 'r', encoding='utf-8') as f:
    broken = f.read()

# The dict needs to be injected INSIDE c.dict, which currently has: en, hi, ta
# Find where to insert: we look for the "Helper for other" comment which is OUTSIDE c.dict
# Actually in the pristine the structure is:
#   c.dict = {
#     en: { ... },
#     hi: { ... },
#     ta: { ... }        <-- last lang dict
#   };
#   // Helper for other 10 Indian languages
#   var fallbackDict = ...

# So we need to insert new dicts BEFORE the closing: `\n    };\n\n    // Helper`
dict_close_marker = "\n    };\n\n    // Helper for other"
if dict_close_marker in cs:
    # Extract the existing ta: {} block from fixed_cs
    lang_codes = ['te', 'kn', 'ml', 'bn', 'mr', 'gu', 'pa', 'or', 'as', 'ur', 'ne', 'sa', 'bho']
    new_dicts_block = ""

    for code in lang_codes:
        # Find in broken: \n        CODE: { ... }
        start_tag = f"\n        {code}: {{"
        si = broken.find(start_tag)
        if si == -1:
            print(f"  ⚠ Dict for '{code}' not found in fixed_cs.js, skipping")
            continue

        # Walk braces to find end of this dict
        brace = 0
        i = si + len(start_tag) - 1  # point at the opening {
        found_end = -1
        while i < len(broken):
            if broken[i] == '{':
                brace += 1
            elif broken[i] == '}':
                brace -= 1
                if brace == 0:
                    found_end = i
                    break
            i += 1

        if found_end == -1:
            print(f"  ⚠ Could not find end of dict for '{code}'")
            continue

        block = broken[si:found_end + 1]  # e.g. \n        te: { ... }
        # Change trailing } to },
        new_dicts_block += block.rstrip() + ",\n"
        print(f"  Extracted dict for '{code}': {found_end - si} chars")

    # Fix: the ta block in pristine ends without comma, we need to add comma before new dicts
    # Find 'ta: {' closing, make sure it has trailing comma
    ta_close_search = broken.find("\n        ta: {")
    ta_brace = 0
    j = ta_close_search + len("\n        ta: {") - 1
    ta_end = -1
    while j < len(broken):
        if broken[j] == '{': ta_brace += 1
        elif broken[j] == '}':
            ta_brace -= 1
            if ta_brace == 0:
                ta_end = j
                break
        j += 1

    if ta_end != -1:
        ta_block = broken[ta_close_search:ta_end+1]
        # Check if ta block is in cs
        if ta_block.rstrip() + "\n    };" in cs:
            # Add comma after ta block and insert new dicts
            cs = cs.replace(ta_block.rstrip() + "\n    };", ta_block.rstrip() + ",\n" + new_dicts_block.rstrip() + "\n    };", 1)
            print("  ✓ Injected all language dicts INSIDE c.dict")
        else:
            # Insert before the closing marker
            cs = cs.replace(dict_close_marker, ",\n" + new_dicts_block.rstrip() + dict_close_marker, 1)
            print("  ✓ Injected language dicts before dict close marker")
    else:
        cs = cs.replace(dict_close_marker, ",\n" + new_dicts_block.rstrip() + dict_close_marker, 1)
        print("  ✓ Injected via fallback")
else:
    print("  ❌ CRITICAL: dict_close_marker not found in pristine cs!")
    sys.exit(1)

# ============================================================
# STEP D: Validate
# ============================================================
print(f"\n[3] Validating... Braces: {cs.count('{')} open vs {cs.count('}')} close")
with open('d:/KPMG/final_cs_v2.js', 'w', encoding='utf-8') as f:
    f.write(cs)

result = subprocess.run(
    ['node', '-c', 'd:/KPMG/final_cs_v2.js'],
    capture_output=True, encoding='utf-8', errors='replace'
)
if result.returncode != 0:
    print("  ❌ SYNTAX ERROR:")
    print(result.stderr[:500] if result.stderr else "(none)")
    sys.exit(1)
print("  ✅ Syntax valid!")

# ============================================================
# STEP E: Deploy
# ============================================================
print("\n[4] Deploying...")
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'client_script': cs}
)
print(f"  Status: {resp.status_code}")
if resp.status_code == 200:
    print("  ✅ DEPLOYED! App should now open normally.")
else:
    print("  ❌ Failed:", resp.text[:300])
