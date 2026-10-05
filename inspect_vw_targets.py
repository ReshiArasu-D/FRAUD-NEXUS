with open('d:/KPMG/build_vw_template.py', 'r', encoding='utf-8') as f:
    text = f.read()

overview_target = '🛡️ INTELLIGENCE STATUS'
verif_target = 'SECTION 3: VERIFICATION QUEUE'

print('Overview target found:', overview_target in text)
print('Verif target found:', verif_target in text)
