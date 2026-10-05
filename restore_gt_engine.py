import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
cs = w['client_script']

# Remove the aggressive removeChild / killBanners function that broke Google Translate!
# Replace with a clean, safe banner hider that only hides the top bar and never deletes Google's worker iframes!

old_killer_start = "// Active MutationObserver to kill the banner iframe"
old_killer_end = "observer.observe(document.documentElement, {"

# Let's find and replace the whole injection block
clean_gt_code = '''
    // SAFE GLOBAL STYLES (Hides only top bar, leaves Google translation worker intact)
    (function injectSafeGtStyles() {
        var existing = document.getElementById('fnx-gt-head-override');
        if (!existing) {
            var style = document.createElement('style');
            style.id = 'fnx-gt-head-override';
            style.type = 'text/css';
            style.innerHTML = [
                '/* HIDE ONLY THE TOP BANNER TOOLBAR */',
                '.goog-te-banner-frame, iframe.goog-te-banner-frame { display: none !important; visibility: hidden !important; height: 0 !important; }',
                '#goog-gt-tt, .goog-te-balloon-frame { display: none !important; visibility: hidden !important; }',
                'body { top: 0px !important; position: static !important; }',
                '.goog-text-highlight { background: none !important; box-shadow: none !important; }'
            ].join('\\n');
            document.head.appendChild(style);
        }
    })();

    // Ensure body.top remains 0 without destroying Google frames
    setInterval(function() {
        if (document.body && document.body.style.top && document.body.style.top !== '0px') {
            document.body.style.top = '0px';
        }
        var banner = document.querySelector('.goog-te-banner-frame');
        if (banner) {
            banner.style.display = 'none';
        }
    }, 250);

    // Google Translate Element Init (All languages enabled, no restriction)
    window.googleTranslateElementInit = function() {
        if (window.google && window.google.translate) {
            new window.google.translate.TranslateElement({
                pageLanguage: 'en',
                layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
                autoDisplay: false
            }, 'google_translate_element');
        }
    };

    // Load Google script if not yet present
    if (!document.getElementById('google-translate-script')) {
        var gtScript = document.createElement('script');
        gtScript.id = 'google-translate-script';
        gtScript.type = 'text/javascript';
        gtScript.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        document.head.appendChild(gtScript);
    }

    // Trigger translation instantly
    c.openGoogleTranslate = function() {
        c.showLangPanel = !c.showLangPanel;
    };

    c.setGoogleTranslateLang = function(langCode) {
        c.currentGtLang = langCode;
        c.showLangPanel = false;

        var domain = window.location.hostname;
        if (langCode === 'en') {
            document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + domain;
            $window.localStorage.removeItem('fnx_gt_lang');
            window.location.reload();
            return;
        }

        // Set cookies so translations persist
        document.cookie = 'googtrans=/en/' + langCode + '; path=/;';
        document.cookie = 'googtrans=/auto/' + langCode + '; path=/;';
        document.cookie = 'googtrans=/en/' + langCode + '; path=/; domain=' + domain;
        document.cookie = 'googtrans=/auto/' + langCode + '; path=/; domain=' + domain;
        $window.localStorage.setItem('fnx_gt_lang', langCode);

        // Find combo and trigger change
        var trigger = function() {
            var combo = document.querySelector('select.goog-te-combo');
            if (combo) {
                combo.value = langCode;
                var evt = document.createEvent('HTMLEvents');
                evt.initEvent('change', true, true);
                combo.dispatchEvent(evt);
                return true;
            }
            return false;
        };

        if (!trigger()) {
            var attempts = 0;
            var poll = setInterval(function() {
                attempts++;
                if (trigger() || attempts > 20) {
                    clearInterval(poll);
                    if (attempts > 20) {
                        // Reload as fallback so cookie takes effect
                        window.location.reload();
                    }
                }
            }, 150);
        }
    };
'''

# Find the entire Google Translate section in client script and replace cleanly
start_marker = "// GLOBAL CSS INJECTION INTO document.head"
if start_marker in cs:
    # Find end of c.setGoogleTranslateLang
    idx_start = cs.find(start_marker)
    # Find auto-restore end
    idx_end = cs.find("// Auto-restore language on load", idx_start)
    if idx_end != -1:
        idx_end = cs.find("}, 800);", idx_end) + len("}, 800);")
    else:
        idx_end = cs.find("}, 1000);", idx_start) + len("}, 1000);")
    cs = cs[:idx_start] + clean_gt_code + cs[idx_end:]
    print("Cleanly replaced Google Translate controller block")
else:
    print("start_marker not found, searching alternative")
    alt = "c.openGoogleTranslate = function() {"
    idx = cs.find(alt)
    print("Found c.openGoogleTranslate at", idx)

resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'client_script': cs}
)
print("Deploy status:", resp.status_code)
