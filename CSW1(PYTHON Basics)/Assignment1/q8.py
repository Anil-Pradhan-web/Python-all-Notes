def validate_password(password):
    errors = []  # to store specific error messages

    # Rule 1: Minimum length 8
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    # Rule 2: At least one uppercase letter
    if not any(ch.isupper() for ch in password):
        errors.append("Password must contain at least one uppercase letter (A–Z).")

    # Rule 3: At least one lowercase letter
    if not any(ch.islower() for ch in password):
        errors.append("Password must contain at least one lowercase letter (a–z).")

    # Rule 4: At least one digit
    if not any(ch.isdigit() for ch in password):
        errors.append("Password must contain at least one digit (0–9).")

    # Rule 5: At least one special character from !@#$%
    special_characters = "!@#$%"
    if not any(ch in special_characters for ch in password):
        errors.append("Password must contain at least one special character (!@#$%).")

    # Rule 6: No whitespace allowed
    if any(ch.isspace() for ch in password):
        errors.append("Password must not contain any spaces.")

    # Final check
    if not errors:
        return True, []
    else:
        return False, errors


# Main Program
password = input("Enter your password: ")
valid, error_messages = validate_password(password)

if valid:
    print("\n✅ Password is VALID.")
else:
    print("\n❌ Password is INVALID. Issues found:")
    for err in error_messages:
        print("-", err)
