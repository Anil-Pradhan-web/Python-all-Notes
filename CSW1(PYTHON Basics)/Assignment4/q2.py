import re

def verify_passwd(s):
    rule1 = re.search(r'[A-Za-z]', s)        # at least one letter
    rule2 = re.search(r'\d', s)              # at least one digit
    rule3 = re.search(r'[@#$%^&*!]', s)      # at least one special char
    rule4 = re.fullmatch(r'[A-Za-z0-9@#$%^&*!]{8,}', s)  # valid chars + length>=8

    return rule1 and rule2 and rule3 and rule4

# Test
tests = ["abc@1234", "Pass123!", "abcd123", "AA11!!aa"]
for t in tests:
    print(t, "→", bool(verify_passwd(t)))
