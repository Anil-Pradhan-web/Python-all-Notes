import random
import string

for i in range(10):
    s = ""
    for j in range(8):
        s += random.choice(string.ascii_lowercase)
    print(s)
