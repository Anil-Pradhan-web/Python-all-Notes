import random

rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

# Generate matrix with random hidden numbers
matrix = [[random.randint(1, 9) for j in range(cols)] for i in range(rows)]

trials = [0] * rows

for i in range(rows):
    hidden = random.choice(matrix[i])
    guess = -1

    while guess != hidden:
        guess = int(input(f"Guess number for row {i+1}: "))
        trials[i] += 1

    print(f"Correct! Row {i+1} guessed in {trials[i]} trials")

print("Trials per row:", trials)
