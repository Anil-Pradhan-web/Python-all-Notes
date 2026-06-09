import random

cards = list(range(52))

random.shuffle(cards)

hand = cards[:5]

print("Dealt cards:", hand)
