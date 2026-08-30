import re
with open('/Users/ljx/Desktop/代码.rtf', 'r') as f:
    text = f.read()

# simple rtf unicode unescape
def unescape_rtf(match):
    return chr(int(match.group(1)))

text = re.sub(r"\\u([0-9]+)\s?", unescape_rtf, text)
with open('parsed.txt', 'w') as f:
    f.write(text)
