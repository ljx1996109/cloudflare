import re
with open('worker/index.js', 'r', encoding='utf-8') as f:
    code = f.read()

new_logic = """											const text = await r.text();
											const arr = text.split('\\n').map(l => l.trim()).filter(Boolean);
											for (const ip of arr) allIps.push(ip);"""

code = re.sub(r"const text = await r\.text\(\);\s*allIps\.push\(\.\.\.text\.split\('\\n'\)\.map\(l => l\.trim\(\)\)\.filter\(Boolean\)\);", new_logic, code)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(code)
