import re

def find_upper_then_digit(s):
    m = re.search(r'([A-Z]).*\d', s)
    if m:
        return m.group(1), m.start(1)

print(find_upper_then_digit("a B blah 9"))
