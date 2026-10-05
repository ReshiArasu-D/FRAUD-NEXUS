import sys

sys.stdout.reconfigure(encoding='utf-8')
lines = open('C:/Users/hp/.gemini/antigravity-ide/brain/59316f90-7827-47e6-86b5-4235fae01a28/FRAUDNEXUS_Spec_Part1.md', 'r', encoding='utf-8').readlines()

# Search for # C., # D., # E.
recording = False
current_sec = ""
for l in lines:
    if l.startswith('# C.') or l.startswith('# D.') or l.startswith('# E.'):
        print("\n" + "="*50)
        print(l.strip())
        print("="*50)
        recording = True
    elif l.startswith('# F.'):
        recording = False
    
    if recording and (l.startswith('## ') or l.startswith('```') or 'LEFT NAVIGATION' in l or 'HEADER' in l or 'INTELLIGENCE PANEL' in l):
        print(l.strip()[:100])
