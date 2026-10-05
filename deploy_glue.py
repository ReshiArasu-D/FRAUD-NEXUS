import requests, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

with open('d:/KPMG/live_widget_client_fresh.js', 'r', encoding='utf-8') as f:
    cs = f.read()

gt_glue = """
    // ====== GOOGLE TRANSLATE PANEL GLUE (used by template) ======
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
    };
"""

old_toggle_end = "    c.toggleLang = function() {\n        var next = c.lang === 'en' ? 'ta' : 'en';\n        c.changeLang(next);\n    };"

if old_toggle_end in cs:
    cs = cs.replace(old_toggle_end, old_toggle_end + '\n' + gt_glue, 1)
    print('Injected GT glue functions after toggleLang')
else:
    print('ERROR: toggleLang marker not found!')

with open('d:/KPMG/test_minimal.js', 'w', encoding='utf-8') as f:
    f.write(cs)

r = subprocess.run(['node', '-c', 'd:/KPMG/test_minimal.js'], capture_output=True, encoding='utf-8', errors='replace')
print('Syntax check:', 'OK' if r.returncode == 0 else r.stderr[:300])

if r.returncode == 0:
    resp = requests.patch(
        f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
        auth=auth,
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        json={'client_script': cs}
    )
    print('Deploy status:', resp.status_code)
    if resp.status_code == 200:
        print('SUCCESS - landing page should now render correctly')
else:
    print('Skipping deploy due to syntax error')
