import re

def normalize_phones(s):
    pattern = r'(?:\+91-|0091\s*|\(91\)\s*|91\s*)?(\d{10})'

    def replace(m):
        num = m.group(1)
        return "+91-" + num

    return re.sub(pattern, replace, s)

text = "Contact: +91-9876543210, Office: (91) 98765 43210, Home: 0091 9876543210"
print(normalize_phones(text))