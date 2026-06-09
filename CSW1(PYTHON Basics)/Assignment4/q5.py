import re

def match_word(w):
    pattern = r'^c[aeiou][^aeiou]$'
    return bool(re.match(pattern, w))

# Test
tests = ["cat", "cit", "cot", "cut", "caa"]
for t in tests:
    print(t, "→", match_word(t))
