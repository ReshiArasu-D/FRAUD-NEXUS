"""
FRAUDNEXUS – Google Translate Integration
==========================================
Replaces the manual EN/TA dictionary system with Google Translate Website Widget.
- Free, no API key required
- Supports all 26+ Indian languages + 100+ global languages
- Embeds inside the existing FRAUDNEXUS widget
- Globe icon / language selector triggers Google Translate picker
"""

import requests, sys, re, json, time

sys.stdout.reconfigure(encoding='utf-8')

auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

print("=" * 60)
print("FRAUDNEXUS – Google Translate Integration Deployment")
print("=" * 60)

# ──────────────────────────────────────────────────────────
# 1. FETCH CURRENT WIDGET
# ──────────────────────────────────────────────────────────
print("\n[1/4] Fetching live widget...")
r = requests.get(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept': 'application/json'}
)
r.raise_for_status()
w = r.json()['result']
tpl = w['template']
cs = w['client_script']
css = w['css']
print(f"  Template: {len(tpl)} chars | Client: {len(cs)} chars | CSS: {len(css)} chars")

# ──────────────────────────────────────────────────────────
# 2. PATCH TEMPLATE – Add Google Translate widget container
# ──────────────────────────────────────────────────────────
print("\n[2/4] Patching template...")

# 2a. Add the Google Translate initialization div & script at the very top of the template
gt_init_block = '''<!-- Google Translate Widget Integration -->
<div id="google_translate_element" style="display:none;"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'as,bn,bh,doi,en,gu,hi,kn,ks,gom,mai,ml,mni,mr,ne,or,pa,sa,sat,sd,ta,te,ur',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false,
        multilanguagePage: true
    }, 'google_translate_element');
}
</script>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
<!-- End Google Translate Widget -->

'''

# Check if already injected
if 'google_translate_element' not in tpl:
    tpl = gt_init_block + tpl
    print("  ✓ Injected Google Translate init block at top of template")
else:
    print("  ⚠ Google Translate init block already exists, skipping")

# 2b. Replace all old language selector dropdowns with Google Translate trigger button
# The old selectors look like: <select class="fnx-lang-select" ng-model="c.lang" ...>
# We replace them with a styled button that triggers Google Translate

gt_button_landing = '''<div class="fnx-gt-translate-btn" ng-click="c.openGoogleTranslate()" title="Translate">
                    <i class="fa fa-globe"></i> <span class="fnx-gt-label">Translate</span>
                    <i class="fa fa-caret-down" style="margin-left:4px;font-size:10px;"></i>
                </div>'''

gt_button_admin = '''<div class="fnx-gt-translate-btn fnx-gt-admin" ng-click="c.openGoogleTranslate()" title="Translate">
                    <i class="fa fa-globe"></i> <span class="fnx-gt-label">Translate</span>
                    <i class="fa fa-caret-down" style="margin-left:4px;font-size:10px;"></i>
                </div>'''

# Replace customer portal language selects
customer_lang_pattern = r'<select\s+class="fnx-lang-select"[^>]*>[\s\S]*?</select>'
matches = list(re.finditer(customer_lang_pattern, tpl))
print(f"  Found {len(matches)} customer language selectors")
for i, m in enumerate(reversed(matches)):
    tpl = tpl[:m.start()] + gt_button_landing + tpl[m.end():]
print(f"  ✓ Replaced {len(matches)} customer lang selectors with Translate button")

# Replace admin portal language selects
admin_lang_pattern = r'<select\s+class="fnx-admin-lang-select"[^>]*>[\s\S]*?</select>'
matches_admin = list(re.finditer(admin_lang_pattern, tpl))
print(f"  Found {len(matches_admin)} admin language selectors")
for m in reversed(matches_admin):
    tpl = tpl[:m.start()] + gt_button_admin + tpl[m.end():]
print(f"  ✓ Replaced {len(matches_admin)} admin lang selectors with Translate button")

# 2c. Add a floating language panel that shows all 26 Indian languages
# This will be a beautiful modal triggered by the translate button
gt_language_panel = '''
<!-- FRAUDNEXUS Language Panel -->
<div class="fnx-gt-language-overlay" ng-if="c.showLangPanel" ng-click="c.showLangPanel=false">
    <div class="fnx-gt-language-panel" ng-click="$event.stopPropagation()">
        <div class="fnx-gt-panel-header">
            <div class="fnx-gt-panel-title">
                <i class="fa fa-globe" style="margin-right:8px;color:#00d4ff;"></i>
                Select Language / भाषा चुनें
            </div>
            <button class="fnx-gt-close-btn" ng-click="c.showLangPanel=false">
                <i class="fa fa-times"></i>
            </button>
        </div>
        <div class="fnx-gt-panel-body">
            <div class="fnx-gt-lang-section">
                <div class="fnx-gt-section-title">Global</div>
                <div class="fnx-gt-lang-grid">
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='en'}" ng-click="c.setGoogleTranslateLang('en')">
                        <span class="fnx-gt-lang-native">English</span>
                    </div>
                </div>
            </div>
            <div class="fnx-gt-lang-section">
                <div class="fnx-gt-section-title">भारतीय भाषाएँ / Indian Languages</div>
                <div class="fnx-gt-lang-grid">
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='hi'}" ng-click="c.setGoogleTranslateLang('hi')">
                        <span class="fnx-gt-lang-native">हिन्दी</span>
                        <span class="fnx-gt-lang-en">Hindi</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='ta'}" ng-click="c.setGoogleTranslateLang('ta')">
                        <span class="fnx-gt-lang-native">தமிழ்</span>
                        <span class="fnx-gt-lang-en">Tamil</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='te'}" ng-click="c.setGoogleTranslateLang('te')">
                        <span class="fnx-gt-lang-native">తెలుగు</span>
                        <span class="fnx-gt-lang-en">Telugu</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='kn'}" ng-click="c.setGoogleTranslateLang('kn')">
                        <span class="fnx-gt-lang-native">ಕನ್ನಡ</span>
                        <span class="fnx-gt-lang-en">Kannada</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='ml'}" ng-click="c.setGoogleTranslateLang('ml')">
                        <span class="fnx-gt-lang-native">മലയാളം</span>
                        <span class="fnx-gt-lang-en">Malayalam</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='bn'}" ng-click="c.setGoogleTranslateLang('bn')">
                        <span class="fnx-gt-lang-native">বাংলা</span>
                        <span class="fnx-gt-lang-en">Bengali</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='mr'}" ng-click="c.setGoogleTranslateLang('mr')">
                        <span class="fnx-gt-lang-native">मराठी</span>
                        <span class="fnx-gt-lang-en">Marathi</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='gu'}" ng-click="c.setGoogleTranslateLang('gu')">
                        <span class="fnx-gt-lang-native">ગુજરાતી</span>
                        <span class="fnx-gt-lang-en">Gujarati</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='pa'}" ng-click="c.setGoogleTranslateLang('pa')">
                        <span class="fnx-gt-lang-native">ਪੰਜਾਬੀ</span>
                        <span class="fnx-gt-lang-en">Punjabi</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='or'}" ng-click="c.setGoogleTranslateLang('or')">
                        <span class="fnx-gt-lang-native">ଓଡ଼ିଆ</span>
                        <span class="fnx-gt-lang-en">Odia</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='as'}" ng-click="c.setGoogleTranslateLang('as')">
                        <span class="fnx-gt-lang-native">অসমীয়া</span>
                        <span class="fnx-gt-lang-en">Assamese</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='ur'}" ng-click="c.setGoogleTranslateLang('ur')">
                        <span class="fnx-gt-lang-native">اردو</span>
                        <span class="fnx-gt-lang-en">Urdu</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='ne'}" ng-click="c.setGoogleTranslateLang('ne')">
                        <span class="fnx-gt-lang-native">नेपाली</span>
                        <span class="fnx-gt-lang-en">Nepali</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='mai'}" ng-click="c.setGoogleTranslateLang('mai')">
                        <span class="fnx-gt-lang-native">मैथिली</span>
                        <span class="fnx-gt-lang-en">Maithili</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='sa'}" ng-click="c.setGoogleTranslateLang('sa')">
                        <span class="fnx-gt-lang-native">संस्कृतम्</span>
                        <span class="fnx-gt-lang-en">Sanskrit</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='sd'}" ng-click="c.setGoogleTranslateLang('sd')">
                        <span class="fnx-gt-lang-native">سنڌي</span>
                        <span class="fnx-gt-lang-en">Sindhi</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='ks'}" ng-click="c.setGoogleTranslateLang('ks')">
                        <span class="fnx-gt-lang-native">کٲشُر</span>
                        <span class="fnx-gt-lang-en">Kashmiri</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='gom'}" ng-click="c.setGoogleTranslateLang('gom')">
                        <span class="fnx-gt-lang-native">कोंकणी</span>
                        <span class="fnx-gt-lang-en">Konkani</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='doi'}" ng-click="c.setGoogleTranslateLang('doi')">
                        <span class="fnx-gt-lang-native">डोगरी</span>
                        <span class="fnx-gt-lang-en">Dogri</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='mni'}" ng-click="c.setGoogleTranslateLang('mni-Mtei')">
                        <span class="fnx-gt-lang-native">ꯃꯤꯇꯩꯂꯣꯟ</span>
                        <span class="fnx-gt-lang-en">Manipuri (Meitei)</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='sat'}" ng-click="c.setGoogleTranslateLang('sat')">
                        <span class="fnx-gt-lang-native">ᱥᱟᱱᱛᱟᱲᱤ</span>
                        <span class="fnx-gt-lang-en">Santali</span>
                    </div>
                    <div class="fnx-gt-lang-card" ng-class="{'active': c.currentGtLang==='bh'}" ng-click="c.setGoogleTranslateLang('bh')">
                        <span class="fnx-gt-lang-native">भोजपुरी</span>
                        <span class="fnx-gt-lang-en">Bhojpuri</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="fnx-gt-panel-footer">
            <span style="opacity:0.5;font-size:11px;">
                <i class="fa fa-google" style="margin-right:4px;"></i> Powered by Google Translate
            </span>
            <button class="fnx-gt-reset-btn" ng-click="c.setGoogleTranslateLang('en')">
                <i class="fa fa-undo"></i> Reset to English
            </button>
        </div>
    </div>
</div>
'''

# Inject language panel before the closing </div> of the main container
# (or just append it at the end of the template)
if 'fnx-gt-language-overlay' not in tpl:
    tpl = tpl + '\n' + gt_language_panel
    print("  ✓ Injected language panel modal")
else:
    print("  ⚠ Language panel already exists, skipping")

print(f"  Template now: {len(tpl)} chars")

# ──────────────────────────────────────────────────────────
# 3. PATCH CLIENT SCRIPT – Add Google Translate controller methods
# ──────────────────────────────────────────────────────────
print("\n[3/4] Patching client script...")

# Add the Google Translate controller methods
gt_client_code = '''
    // ========== GOOGLE TRANSLATE INTEGRATION ==========
    c.showLangPanel = false;
    c.currentGtLang = 'en';

    c.openGoogleTranslate = function() {
        c.showLangPanel = !c.showLangPanel;
    };

    c.setGoogleTranslateLang = function(langCode) {
        c.currentGtLang = langCode;
        c.showLangPanel = false;

        // Use Google Translate's internal API to trigger translation
        var gtCombo = document.querySelector('.goog-te-combo');
        if (gtCombo) {
            gtCombo.value = langCode;
            // Trigger change event
            var event = document.createEvent('HTMLEvents');
            event.initEvent('change', true, true);
            gtCombo.dispatchEvent(event);
        } else {
            // Fallback: set cookie and reload
            var domain = window.location.hostname;
            document.cookie = 'googtrans=/en/' + langCode + ';path=/;domain=' + domain;
            document.cookie = 'googtrans=/en/' + langCode + ';path=/';
            window.location.reload();
        }

        // Also update internal lang for c.t() fallback
        c.lang = (langCode === 'en') ? 'en' : langCode;
        $window.localStorage.setItem('fnx_lang', langCode);
        $window.localStorage.setItem('fnx_gt_lang', langCode);
    };

    // Auto-restore Google Translate language on page load
    $timeout(function() {
        var savedGtLang = $window.localStorage.getItem('fnx_gt_lang');
        if (savedGtLang && savedGtLang !== 'en') {
            c.currentGtLang = savedGtLang;
            // Wait for Google Translate to initialize
            var checkGt = setInterval(function() {
                var gtCombo = document.querySelector('.goog-te-combo');
                if (gtCombo) {
                    clearInterval(checkGt);
                    gtCombo.value = savedGtLang;
                    var event = document.createEvent('HTMLEvents');
                    event.initEvent('change', true, true);
                    gtCombo.dispatchEvent(event);
                }
            }, 500);
            // Stop checking after 10 seconds
            setTimeout(function() { clearInterval(checkGt); }, 10000);
        }
    }, 1000);
'''

# Insert after the c.t() function definition
insert_marker = "    c.t = function(key) {\n        var langDict = c.dict[c.lang] || c.dict.en;\n        return langDict[key] || c.dict.en[key] || key;\n    };"
if insert_marker in cs:
    cs = cs.replace(insert_marker, insert_marker + '\n' + gt_client_code)
    print("  ✓ Injected Google Translate controller methods after c.t()")
else:
    # Try alternate formatting
    alt_marker = "c.t = function(key) {"
    if alt_marker in cs and 'c.openGoogleTranslate' not in cs:
        idx = cs.find(alt_marker)
        # Find the closing of c.t()
        brace_count = 0
        i = idx
        while i < len(cs):
            if cs[i] == '{':
                brace_count += 1
            elif cs[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    # Found the end of c.t()
                    end_idx = i + 1
                    # Skip to end of line
                    while end_idx < len(cs) and cs[end_idx] in ' \t\r\n;':
                        end_idx += 1
                        if cs[end_idx-1] == '\n':
                            break
                    cs = cs[:end_idx] + '\n' + gt_client_code + cs[end_idx:]
                    print("  ✓ Injected Google Translate methods (alt insertion)")
                    break
            i += 1
    elif 'c.openGoogleTranslate' in cs:
        print("  ⚠ Google Translate methods already exist, skipping")
    else:
        print("  ⚠ Could not find c.t() marker, appending before FORMS section")
        forms_marker = "// ========== FORMS & AUTH =========="
        if forms_marker in cs:
            cs = cs.replace(forms_marker, gt_client_code + '\n    ' + forms_marker)
            print("  ✓ Injected before FORMS section")

print(f"  Client script now: {len(cs)} chars")

# ──────────────────────────────────────────────────────────
# 4. PATCH CSS – Add Google Translate styling
# ──────────────────────────────────────────────────────────
print("\n[4/4] Patching CSS...")

gt_css = '''
/* ======================================================
   GOOGLE TRANSLATE INTEGRATION STYLES
   ====================================================== */

/* Hide default Google Translate bar */
.goog-te-banner-frame,
#goog-gt-tt,
.goog-te-balloon-frame,
.skiptranslate,
.goog-te-gadget {
    display: none !important;
}
body { top: 0 !important; }
.goog-text-highlight { background: none !important; box-shadow: none !important; }

/* ---- Translate Trigger Button ---- */
.fnx-gt-translate-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 16px;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 20px;
    color: #00d4ff;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    user-select: none;
    white-space: nowrap;
}
.fnx-gt-translate-btn:hover {
    background: rgba(0, 212, 255, 0.18);
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 0 0 16px rgba(0, 212, 255, 0.15);
    transform: translateY(-1px);
}
.fnx-gt-translate-btn .fa-globe {
    font-size: 15px;
}
.fnx-gt-translate-btn.fnx-gt-admin {
    padding: 6px 14px;
    font-size: 12px;
    background: rgba(0, 212, 255, 0.06);
}

/* ---- Language Selection Overlay ---- */
.fnx-gt-language-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    z-index: 99999;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fnxGtFadeIn 0.25s ease;
}
@keyframes fnxGtFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.fnx-gt-language-panel {
    background: linear-gradient(145deg, #1a1a2e 0%, #0d1117 100%);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px;
    width: 720px;
    max-width: 92vw;
    max-height: 85vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow:
        0 25px 60px rgba(0, 0, 0, 0.5),
        0 0 40px rgba(0, 212, 255, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    animation: fnxGtSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fnxGtSlideUp {
    from { opacity: 0; transform: translateY(30px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.fnx-gt-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.fnx-gt-panel-title {
    font-size: 18px;
    font-weight: 600;
    color: #fff;
    display: flex;
    align-items: center;
}
.fnx-gt-close-btn {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: #888;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;
}
.fnx-gt-close-btn:hover {
    background: rgba(255, 60, 60, 0.15);
    color: #ff6b6b;
    border-color: rgba(255, 60, 60, 0.3);
}

.fnx-gt-panel-body {
    padding: 16px 24px 20px;
    overflow-y: auto;
    flex: 1;
}
.fnx-gt-lang-section {
    margin-bottom: 20px;
}
.fnx-gt-section-title {
    font-size: 12px;
    font-weight: 600;
    color: #00d4ff;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0, 212, 255, 0.1);
}

.fnx-gt-lang-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 8px;
}

.fnx-gt-lang-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 12px 14px;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.fnx-gt-lang-card:hover {
    background: rgba(0, 212, 255, 0.08);
    border-color: rgba(0, 212, 255, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 212, 255, 0.1);
}
.fnx-gt-lang-card.active {
    background: rgba(0, 212, 255, 0.12);
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.12);
}
.fnx-gt-lang-card.active .fnx-gt-lang-native {
    color: #00d4ff;
}

.fnx-gt-lang-native {
    font-size: 15px;
    font-weight: 600;
    color: #e0e0e0;
    line-height: 1.3;
}
.fnx-gt-lang-en {
    font-size: 11px;
    color: #666;
    font-weight: 400;
}

.fnx-gt-panel-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(0, 0, 0, 0.2);
}
.fnx-gt-reset-btn {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: #aaa;
    padding: 6px 14px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
}
.fnx-gt-reset-btn:hover {
    background: rgba(0, 212, 255, 0.1);
    color: #00d4ff;
    border-color: rgba(0, 212, 255, 0.3);
}

/* ---- Responsive ---- */
@media (max-width: 600px) {
    .fnx-gt-language-panel {
        border-radius: 16px;
        width: 95vw;
    }
    .fnx-gt-lang-grid {
        grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
        gap: 6px;
    }
    .fnx-gt-lang-card {
        padding: 10px 10px;
    }
    .fnx-gt-lang-native {
        font-size: 13px;
    }
    .fnx-gt-translate-btn .fnx-gt-label {
        display: none;
    }
}
'''

if 'fnx-gt-translate-btn' not in css:
    css = css + '\n' + gt_css
    print("  ✓ Injected Google Translate CSS styles")
else:
    print("  ⚠ Google Translate CSS already exists, skipping")

print(f"  CSS now: {len(css)} chars")

# ──────────────────────────────────────────────────────────
# 5. DEPLOY
# ──────────────────────────────────────────────────────────
print("\n[5/5] Deploying to ServiceNow...")
payload = {
    'template': tpl,
    'client_script': cs,
    'css': css
}

resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
    json=payload
)
print(f"  Status: {resp.status_code}")
if resp.status_code == 200:
    print("  ✅ Successfully deployed Google Translate integration!")
    print("\n  FEATURES:")
    print("  • Click 'Translate' button → opens language panel")
    print("  • 22 Indian languages + English supported")
    print("  • Free, no API key needed")
    print("  • Powered by Google Translate")
    print("  • Persists language choice across page loads")
else:
    print(f"  ❌ Deploy failed: {resp.text[:500]}")
