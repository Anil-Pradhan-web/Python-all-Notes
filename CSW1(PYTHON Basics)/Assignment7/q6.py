import random

def spin_wheel():
    count = [0] * 6

    for i in range(2000):
        n = random.randint(1, 6)
        count[n-1] += 1

    for i in range(6):
        print("Segment", i+1,
              "Count:", count[i],
              "Probability:", count[i]/2000)

    print("Highest appearance:", count.index(max(count)) + 1)
    print("Lowest appearance:", count.index(min(count)) + 1)

spin_wheel()
