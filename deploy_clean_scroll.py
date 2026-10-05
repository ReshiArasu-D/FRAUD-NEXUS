import requests, sys

sys.stdout.reconfigure(encoding='utf-8')
auth = ('admin', 'mn%XC1^ScdA4')
base = 'https://dev187180.service-now.com'
WIDGET_ID = '2f258577c32b43d0e54832f1b401317f'

r = requests.get(f'{base}/api/now/table/sp_widget/{WIDGET_ID}', auth=auth, headers={'Accept':'application/json'})
w = r.json()['result']
css = w['css']

clean_scroll_and_banner_css = '''
/* =====================================================================
   CLEAN SINGLE-SCROLL & GOOGLE BANNER SUPPRESSION (FRAUDNEXUS)
   ===================================================================== */

/* 1. HIDE GOOGLE TRANSLATE BANNER & FRAMES COMPLETELY */
iframe.goog-te-banner-frame,
iframe.skiptranslate,
.goog-te-banner-frame,
.goog-te-banner,
#goog-gt-tt,
.goog-te-balloon-frame,
.goog-tooltip,
.goog-tooltip:hover,
div#goog-gt-,
body > .skiptranslate {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    position: absolute !important;
    top: -9999px !important;
    left: -9999px !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* 2. PREVENT BODY DISPLACEMENT */
body {
    top: 0px !important;
    position: static !important;
}

/* 3. ELIMINATE TRIPLE/DUPLICATE SCROLLBARS */
html,
body,
.page,
#page_content,
.sp-page-root {
    overflow: hidden !important;
    height: 100vh !important;
    max-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Custom sleek scrollbar for the internal scrollable container only */
.fnx-landing::-webkit-scrollbar,
.fnx-admin-main-content::-webkit-scrollbar,
.fnx-admin-sidebar::-webkit-scrollbar {
    width: 6px;
}
.fnx-landing::-webkit-scrollbar-track,
.fnx-admin-main-content::-webkit-scrollbar-track,
.fnx-admin-sidebar::-webkit-scrollbar-track {
    background: rgba(10, 15, 29, 0.6);
}
.fnx-landing::-webkit-scrollbar-thumb,
.fnx-admin-main-content::-webkit-scrollbar-thumb,
.fnx-admin-sidebar::-webkit-scrollbar-thumb {
    background: rgba(0, 212, 255, 0.25);
    border-radius: 4px;
}
.fnx-landing::-webkit-scrollbar-thumb:hover,
.fnx-admin-main-content::-webkit-scrollbar-thumb:hover,
.fnx-admin-sidebar::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 212, 255, 0.5);
}
'''

css = css + '\n' + clean_scroll_and_banner_css

resp = requests.patch(
    f'{base}/api/now/table/sp_widget/{WIDGET_ID}',
    auth=auth,
    headers={'Accept':'application/json', 'Content-Type':'application/json'},
    json={'css': css}
)
print("Updated CSS with strict single-scroll & banner suppression! Status:", resp.status_code)
