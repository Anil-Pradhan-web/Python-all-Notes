import sys

args = sys.argv[1:]
try:
    total = sum(float(a) for a in args)
    print("Sum of numbers:", total)
except ValueError as e:
    print("Error: Please enter only valid numbers.")
