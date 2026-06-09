import random

heads = 0
tails = 0

for i in range(1000):
    toss = random.choice(["H", "T"])
    if toss == "H":
        heads += 1
    else:
        tails += 1

print("Heads:", heads)
print("Tails:", tails)
print("Probability of Heads:", heads/1000)
print("Probability of Tails:", tails/1000)
