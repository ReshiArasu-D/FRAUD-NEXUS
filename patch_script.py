with open('d:/KPMG/fix_ui_visibility.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('template = f"""')
if pos > 0:
    part1 = text[:pos]
    part2 = text[pos:]
    part2 = part2.replace('template = f"""', 'template_raw = r"""', 1)
    part2 = part2.replace('{{{{', '{{').replace('}}}}', '}}')
    part2 = part2.replace('{css_content}', '/* CSS_PLACEHOLDER */')
    deploy_pos = part2.find('# ============================================================\n# DEPLOY TO SERVICENOW')
    if deploy_pos > 0:
        part2 = part2[:deploy_pos] + 'template = template_raw.replace("/* CSS_PLACEHOLDER */", css_content)\n\n' + part2[deploy_pos:]
    with open('d:/KPMG/fix_ui_visibility.py', 'w', encoding='utf-8') as out:
        out.write(part1 + part2)
    print("SUCCESS: fix_ui_visibility.py converted to raw string replacement")
else:
    print("Could not find template = f\"\"\"")
