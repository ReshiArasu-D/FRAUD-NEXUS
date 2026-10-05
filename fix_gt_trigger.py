import requests, sys, re

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
tpl = w['template']
cs = w['client_script']

# 1. FIX TEMPLATE: Replace display:none with off-screen positioning so Google actually renders .goog-te-combo
old_gt_element_regex = r'<!-- Google Translate Widget Integration -->[\s\S]*?<!-- End Google Translate Widget -->'
new_gt_element = '''<!-- Google Translate Widget Integration -->
<div id="google_translate_element" style="position:fixed;bottom:-9999px;right:-9999px;width:10px;height:10px;overflow:hidden;opacity:0.01;pointer-events:none;z-index:-9999;"></div>
<!-- End Google Translate Widget -->'''

if re.search(old_gt_element_regex, tpl):
    tpl = re.sub(old_gt_element_regex, new_gt_element, tpl)
    print("Replaced Google Translate element in template with off-screen container")
elif '<div id="google_translate_element"' in tpl:
    tpl = re.sub(r'<div id="google_translate_element"[^>]*>[\s\S]*?</div>', new_gt_element, tpl)
    print("Replaced raw div in template")

# 2. FIX CLIENT SCRIPT: Solid initialization and instant translation trigger without page reload
# Find setGoogleTranslateLang block in cs
pattern = r'c\.setGoogleTranslateLang\s*=\s*function\(langCode\)\s*\{[\s\S]*?auto-restore[\s\S]*?\}\);\s*\}'

new_set_lang_code = '''c.setGoogleTranslateLang = function(langCode) {
        c.currentGtLang = langCode;
        c.showLangPanel = false;

        // Set translation cookies
        var domain = window.location.hostname;
        if (langCode === 'en') {
            document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + domain;
            $window.localStorage.removeItem('fnx_gt_lang');
            // Try to find show original iframe button or reload once to restore original
            var restoreBtn = document.querySelector('.goog-te-banner-frame');
            if (restoreBtn) {
                try {
                    var doc = restoreBtn.contentDocument || restoreBtn.contentWindow.document;
                    var btn = doc.querySelector('.goog-te-button button') || doc.querySelector('#\\\\:1\\\\.restore');
                    if (btn) { btn.click(); return; }
                } catch(e) {}
            }
            window.location.reload();
            return;
        }

        // For target language:
        document.cookie = 'googtrans=/en/' + langCode + '; path=/;';
        document.cookie = 'googtrans=/auto/' + langCode + '; path=/;';
        document.cookie = 'googtrans=/en/' + langCode + '; path=/; domain=' + domain;
        document.cookie = 'googtrans=/auto/' + langCode + '; path=/; domain=' + domain;
        $window.localStorage.setItem('fnx_gt_lang', langCode);
        $window.localStorage.setItem('fnx_lang', langCode);

        // Attempt triggering .goog-te-combo directly
        var applyTranslation = function() {
            var combo = document.querySelector('select.goog-te-combo');
            if (combo) {
                combo.value = langCode;
                // Trigger change event for Google Translate
                if (typeof Event === 'function') {
                    combo.dispatchEvent(new Event('change', { bubbles: true }));
                }
                var evt = document.createEvent('HTMLEvents');
                evt.initEvent('change', true, true);
                combo.dispatchEvent(evt);
                return true;
            }
            return false;
        };

        // Try immediately
        if (!applyTranslation()) {
            // Poll for up to 3 seconds for Google script to populate combo
            var attempts = 0;
            var pollTimer = setInterval(function() {
                attempts++;
                if (applyTranslation() || attempts >= 30) {
                    clearInterval(pollTimer);
                    if (attempts >= 30 && !document.querySelector('select.goog-te-combo')) {
                        // Only reload if Google Translate script failed to mount after 3s
                        window.location.reload();
                    }
                }
            }, 100);
        }
    };

    // Auto-restore language on load without reload loop
    $timeout(function() {
        var savedGtLang = $window.localStorage.getItem('fnx_gt_lang');
        if (savedGtLang && savedGtLang !== 'en') {
            c.currentGtLang = savedGtLang;
            var checkAttempts = 0;
            var initTimer = setInterval(function() {
                checkAttempts++;
                var combo = document.querySelector('select.goog-te-combo');
                if (combo) {
                    clearInterval(initTimer);
                    combo.value = savedGtLang;
                    var evt = document.createEvent('HTMLEvents');
                    evt.initEvent('change', true, true);
                    combo.dispatchEvent(evt);
                } else if (checkAttempts > 40) {
                    clearInterval(initTimer);
                }
            }, 150);
        }
    }, 800);'''

# Replace the method in cs
start_pos = cs.find("c.setGoogleTranslateLang = function(langCode) {")
if start_pos != -1:
    # Find the end of auto-restore
    end_marker = "}, 1000);"
    end_pos = cs.find(end_marker, start_pos)
    if end_pos != -1:
        end_pos += len(end_marker)
        cs = cs[:start_pos] + new_set_lang_code + cs[end_pos:]
        print("Replaced setGoogleTranslateLang and auto-restore in client script")
    else:
        print("Could not find end marker for setGoogleTranslateLang")
else:
    print("Could not find start pos of setGoogleTranslateLang")

# 3. Deploy
print("Deploying updated widget...")
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'template': tpl, 'client_script': cs}
)
print("Deploy status:", resp.status_code)
