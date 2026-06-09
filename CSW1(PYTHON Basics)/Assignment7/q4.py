import random

freq = [0] * 10

for i in range(5000):
    num = random.randint(0, 9)
    freq[num] += 1

expected = 5000 / 10

for i in range(10):
    print("Digit:", i,
          "Count:", freq[i],
          "Ratio:", freq[i] / expected)
