import re
with open('worker/index.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix text.split('\n')
code = re.sub(r"text\.split\('\n'\)", r"text.split('\\n')", code)
# Fix replace regex
code = re.sub(r"ip\.replace\(\/\[\t\"'\n\]\+\/g", r"ip.replace(/[\\t\"\'\\n]+/g", code)
# Fix join('\n')
code = re.sub(r"join\('\n'\)", r"join('\\n')", code)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(code)
