import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('d:/KPMG/widget_backup_before_analytics.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tpl = d['template']

idx_main = tpl.find('<main class="fnx-content"')
idx_track = tpl.find("c.currentView === 'trackCases'", 50000)

print(f"Main starts at: {idx_main}")
print(f"Track starts at: {idx_track}")

# Let's search for </main> between idx_main and idx_track
idx_close_main = tpl.find("</main>", idx_main)
print(f"</main> found at: {idx_close_main}")

# Let's see what is around idx_close_main
print("Around </main>:")
print(tpl[max(0, idx_close_main-200):min(len(tpl), idx_close_main+200)])
