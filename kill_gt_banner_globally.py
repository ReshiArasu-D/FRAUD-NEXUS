import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
cs = w['client_script']

# Inject global style sheet into document.head via JS
global_style_injector = '''
    // GLOBAL CSS INJECTION INTO document.head TO DEFEAT SERVICENOW SCOPING
    (function injectGlobalGtFix() {
        var existing = document.getElementById('fnx-gt-head-override');
        if (!existing) {
            var style = document.createElement('style');
            style.id = 'fnx-gt-head-override';
            style.type = 'text/css';
            style.innerHTML = [
                '/* OBLITERATE GOOGLE TRANSLATE TOP BAR GLOBALLY */',
                '.goog-te-banner-frame, iframe.goog-te-banner-frame, .goog-te-banner, #goog-gt-tt, .goog-te-balloon-frame {',
                '    display: none !important;',
                '    visibility: hidden !important;',
                '    height: 0 !important;',
                '    width: 0 !important;',
                '    border: none !important;',
                '    top: -9999px !important;',
                '    left: -9999px !important;',
                '    position: absolute !important;',
                '    opacity: 0 !important;',
                '    pointer-events: none !important;',
                '}',
                'body {',
                '    top: 0px !important;',
                '    position: static !important;',
                '}',
                '/* HIDE ANY SKIPTRANSLATE IFRAME THAT HOVERS AT TOP */',
                'iframe.skiptranslate, body > .skiptranslate {',
                '    display: none !important;',
                '}',
                '.goog-text-highlight {',
                '    background: none !important;',
                '    box-shadow: none !important;',
                '}'
            ].join('\\n');
            document.head.appendChild(style);
        }
    })();

    // Active MutationObserver to kill the banner iframe whenever Google creates it
    (function observeGtBanner() {
        var killBanners = function() {
            if (document.body) {
                if (document.body.style.top && document.body.style.top !== '0px') {
                    document.body.style.top = '0px';
                }
            }
            var frames = document.querySelectorAll('.goog-te-banner-frame, iframe[name*="container"], iframe.skiptranslate');
            for (var i = 0; i < frames.length; i++) {
                frames[i].style.setProperty('display', 'none', 'important');
                frames[i].style.setProperty('height', '0px', 'important');
                frames[i].style.setProperty('visibility', 'hidden', 'important');
                if (frames[i].parentNode) {
                    frames[i].parentNode.removeChild(frames[i]);
                }
            }
        };

        // Run immediately and every 100ms for first 5 seconds, then every 400ms
        killBanners();
        var timer = setInterval(killBanners, 200);

        // Also use MutationObserver if available
        if (window.MutationObserver) {
            var observer = new MutationObserver(killBanners);
            observer.observe(document.documentElement, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['style', 'class']
            });
        }
    })();
'''

# Find insertion point in cs
target_marker = "window.googleTranslateElementInit = function() {"
if target_marker in cs:
    cs = cs.replace(target_marker, global_style_injector + '\n    ' + target_marker)
    print("Replaced before googleTranslateElementInit")
else:
    # Alternative: insert right at top of controller
    cs = global_style_injector + '\n' + cs
    print("Injected at top of controller")

resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'client_script': cs}
)
print("Updated! Status:", resp.status_code)
