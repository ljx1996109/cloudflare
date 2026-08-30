import re
with open('worker/index.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("join('\n')", "join('\\n')")

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(code)
