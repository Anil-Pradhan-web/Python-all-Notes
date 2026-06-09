import random

count = {}

for i in range(10000):
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    s = d1 + d2

    if s in count:
        count[s] += 1
    else:
        count[s] = 1

for s in range(2, 13):
    print("Sum", s, "Probability =", count[s] / 10000)
