import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
css = w['css']
cs = w['client_script']

# 1. ENHANCED CSS TO COMPLETELY OBLITERATE GOOGLE BANNER AND EXTRA SCROLLBARS
css_fix = '''
/* ======================================================
   FORCE HIDE ALL GOOGLE TRANSLATE BANNERS & FIX SCROLLBARS
   ====================================================== */
iframe.goog-te-banner-frame,
.goog-te-banner-frame,
.goog-te-banner-frame.skiptranslate,
.goog-te-banner,
#goog-gt-tt,
.goog-te-balloon-frame,
.goog-tooltip,
.goog-tooltip:hover,
div#goog-gt-,
.skiptranslate:not(.fnx-gt-preserve) {
    display: none !important;
    visibility: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 0 !important;
    width: 0 !important;
    line-height: 0 !important;
    border: none !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Force body top to 0 and fix scrollbar duplication */
html {
    overflow-x: hidden !important;
    height: 100% !important;
}

body {
    top: 0px !important;
    position: static !important;
    min-height: 100% !important;
    overflow-x: hidden !important;
}

/* Remove unwanted Google highlight style */
.goog-text-highlight {
    background: transparent !important;
    box-shadow: none !important;
}
'''

# 2. Add mutation observer in client script to immediately destroy the top banner iframe and keep body.top = 0
js_banner_remover = '''
    // Continuously suppress Google Translate banner iframe and body shift
    var suppressGtBanner = function() {
        if (document.body && document.body.style.top !== '0px') {
            document.body.style.top = '0px';
        }
        var iframes = document.querySelectorAll('iframe.goog-te-banner-frame, iframe[name*="container"]');
        for (var i = 0; i < iframes.length; i++) {
            iframes[i].style.display = 'none';
            iframes[i].style.height = '0px';
            iframes[i].style.visibility = 'hidden';
            if (iframes[i].parentNode) {
                iframes[i].parentNode.removeChild(iframes[i]);
            }
        }
    };
    setInterval(suppressGtBanner, 300);
'''

# Append CSS fix
css = css + '\n' + css_fix

# Insert JS fix into client script
if 'suppressGtBanner' not in cs:
    cs = cs.replace("c.openGoogleTranslate = function() {", js_banner_remover + '\n    c.openGoogleTranslate = function() {')

print("Updating widget...")
resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'css': css, 'client_script': cs}
)
print("Updated! Status:", resp.status_code)
