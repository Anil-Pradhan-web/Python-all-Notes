import re

pattern = r'^[a-z]+[0-9]+$'

tests = ["abc123", "a1b2", "ABC123"]
for t in tests:
    print(t, "→", bool(re.match(pattern, t)))
