import re

def find_repeated_letters(s):
    pattern = r'(.)\1+'
    for m in re.finditer(pattern, s):
        print("Sequence:", m.group(0),
              " Letter:", m.group(1),
              " Span:", m.span())

find_repeated_letters("hellooo baad zzzy")

