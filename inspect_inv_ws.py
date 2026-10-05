import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('d:/KPMG/current_deployed_template.html', 'r', encoding='utf-8') as f:
    t = f.read()

start = t.find("class=\"fnx-investigation-workspace\"")
if start != -1:
    end = t.find("<!-- ====================================================", start + 500)
    print("Investigation block found, length:", end - start)
    print(t[start:start+2500])
else:
    print("Not found")
