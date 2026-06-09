import string
# -----------------------------------------------------
# Function 1: Check palindrome using for loop
def is_palindrome_for_loop(s):
    s = s.lower()  # ignore case
    length = len(s)
    for i in range(length // 2):
        if s[i] != s[length - i - 1]:
            return False
    return True
# -----------------------------------------------------
# Function 2: Check palindrome using two-pointer technique
def is_palindrome_two_pointer(s):
    # Step 1: Clean the string
    cleaned = ""
    for ch in s:
        if ch.isalnum():          # take only letters and digits
            cleaned += ch.lower()  # make it lowercase
    
    # Step 2: Check if cleaned string equals its reverse
    if cleaned == cleaned[::-1]:
        return True
    else:
        return False

# Main program
text = input("Enter a string: ")

# Call both functions
result_for = is_palindrome_for_loop(text)
result_two_pointer = is_palindrome_two_pointer(text)
# Display results
print(f"For-loop Check      : {"Palindrome" if result_for else "Not Palindrome"}")
print(f"Two-pointer Check   : {'Palindrome' if result_two_pointer else 'Not Palindrome'}")