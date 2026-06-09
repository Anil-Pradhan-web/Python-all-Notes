import re

def extract_date_parts(s):
    m = re.search(r'(\d{2})-(\d{2})-(\d{4})', s)
    if m:
        return (m.group(0), m.group(1), m.group(2), m.group(3),
                m.span(), m.lastindex)

print(extract_date_parts("Backup 05-11-2025 complete"))
