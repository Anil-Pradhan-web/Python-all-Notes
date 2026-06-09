import re

s = "1 set of 23 owls, 999 doves."
m = re.search(r'\d{2,}', s)

if m:
    print(f'"{m.group()}" found at {m.span()}')
