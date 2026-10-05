import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
cs = r.json()['result']['client_script']

dynamic_loader = '''
    // Dynamic Google Translate Script Loader (ensures execution in Service Portal)
    window.googleTranslateElementInit = function() {
        if (window.google && window.google.translate) {
            new window.google.translate.TranslateElement({
                pageLanguage: 'en',
                includedLanguages: 'as,bn,bh,doi,en,gu,hi,kn,ks,gom,mai,ml,mni,mr,ne,or,pa,sa,sat,sd,ta,te,ur',
                layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
                autoDisplay: false,
                multilanguagePage: true
            }, 'google_translate_element');
        }
    };

    if (!document.getElementById('google-translate-script')) {
        var gtScript = document.createElement('script');
        gtScript.id = 'google-translate-script';
        gtScript.type = 'text/javascript';
        gtScript.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        document.head.appendChild(gtScript);
    }
'''

# Check if already present
if 'google-translate-script' not in cs:
    target = "c.openGoogleTranslate = function() {"
    if target in cs:
        cs = cs.replace(target, dynamic_loader + '\n    ' + target)
        resp = requests.patch(
            f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
            auth=auth,
            headers={'Accept':'application/json', 'Content-Type':'application/json'},
            json={'client_script': cs}
        )
        print("Dynamic loader injected! Status:", resp.status_code)
    else:
        print("Target marker not found in cs")
else:
    print("Dynamic loader already in client script")
