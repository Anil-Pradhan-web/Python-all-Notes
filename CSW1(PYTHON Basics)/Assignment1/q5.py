# Step 1: Read decimal number from user
decimal_num = int(input("Enter a decimal number: "))

# Step 2: Convert to Binary, Octal, and Hexadecimal (without prefixes)
binary_str = bin(decimal_num)[2:]      # remove '0b'
octal_str = oct(decimal_num)[2:]       # remove '0o'
hexadecimal_str = hex(decimal_num)[2:] # remove '0x'

# Step 3: Count digits in each converted representation
binary_count = len(binary_str)
octal_count = len(octal_str)
hexadecimal_count = len(hexadecimal_str)

# Step 4: Reverse conversion back to decimal
binary_to_decimal = int(binary_str, 2)
octal_to_decimal = int(octal_str, 8)
hexadecimal_to_decimal = int(hexadecimal_str, 16)

# Step 5: Display results
print("\n--- Base Conversion Results ---")
print(f"Decimal Number: {decimal_num}")
print(f"Binary        : {binary_str} (Digits: {binary_count})")
print(f"Octal         : {octal_str} (Digits: {octal_count})")
print(f"Hexadecimal   : {hexadecimal_str.upper()} (Digits: {hexadecimal_count})")

print("\n--- Reverse Conversion Check ---")
print(f"Binary to Decimal      : {binary_to_decimal}")
print(f"Octal to Decimal       : {octal_to_decimal}")
print(f"Hexadecimal to Decimal : {hexadecimal_to_decimal}")