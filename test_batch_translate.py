import requests, json, sys, re, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

# Test translating a batch of keys with Google Translate API
def translate_texts(texts, target_lang):
    # Join with newlines
    combined = '\n'.join(texts)
    encoded = urllib.parse.quote(combined)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={encoded}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        translated_parts = [item[0] for item in data[0] if item[0]]
        full_translated = ''.join(translated_parts)
        lines = full_translated.split('\n')
        # Ensure same length
        if len(lines) == len(texts):
            return lines
        else:
            return [item[0] for item in data[0]]
    except Exception as e:
        print(f"Error for {target_lang}: {e}")
        return texts

sample = ["Financial & Cyber Fraud Investigation Hub", "Command Center", "Partners", "Customer Portal"]
res_hi = translate_texts(sample, 'hi')
res_ta = translate_texts(sample, 'ta')
print("HI:", res_hi[:2])
print("TA:", res_ta[:2])
