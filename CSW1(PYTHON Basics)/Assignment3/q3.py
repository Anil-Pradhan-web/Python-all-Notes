input_str = input("Enter integers separated by spaces: ")

# Convert input string to a list of integers
numbers = list(map(int, input_str.split()))

# Ensure the list has at least 3 numbers for unpacking in the middle
if len(numbers) < 3:
    print("Please enter at least 3 integers for this operation.")
else:
    # Tuple unpacking with starred expression at the start
    first, second, *remaining = numbers

    # Display the extracted values
    print("First number: %d" % first)
    print("Second number: %d" % second)
    print("Remaining numbers: %s" % remaining)

    # Swap the first two numbers
    first, second = second, first
    print("After swapping: First: %d, Second: %d" % (first, second))

    # Compute and print the sum of the remaining numbers
    sum_remaining = sum(remaining)
    print("Sum of remaining numbers: %d" % sum_remaining)

    # Demonstrate unpacking with starred variable in the middle using user input
    first_val, *middle_vals, last_val = numbers
    print("\nUnpacking with starred variable in the middle:")
    print("First: %d" % first_val)
    print("Middle: %s" % middle_vals)
    print("Last: %d" % last_val)