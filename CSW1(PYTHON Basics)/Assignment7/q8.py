import random
import string

freq = {}

for i in range(100):
    ch = random.choice(string.ascii_lowercase)
    if ch in freq:
        freq[ch] += 1
    else:
        freq[ch] = 1

for ch in freq:
    print(ch, "Count:", freq[ch], "Frequency:", freq[ch]/100)
