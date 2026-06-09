def encrypt(text):
    # Step 1: Reverse the string
    reversed_text = text[::-1]
    encrypted = ""
    i = 0
    while i < len(reversed_text):
        if i + 1 < len(reversed_text):
            encrypted += reversed_text[i + 1] + reversed_text[i]  # swap
            i += 2
        else:
            encrypted += reversed_text[i]  # last single character (if odd length)
            i += 1
    return encrypted

def decrypt(encrypted_text):
    # Step 1: Swap back every adjacent pair
    swapped_back = ""
    i = 0
    while i < len(encrypted_text):
        if i + 1 < len(encrypted_text):
            swapped_back += encrypted_text[i + 1] + encrypted_text[i]
            i += 2
        else:
            swapped_back += encrypted_text[i]
            i += 1
    # Step 2: Reverse again to get original text
    original = swapped_back[::-1]
    return original

# Main program
text = input("Enter a string: ")

encrypted = encrypt(text)
decrypted = decrypt(encrypted)

print(f"\nEncrypted: {encrypted}")
print(f"Decrypted: {decrypted}")