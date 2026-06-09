def process_paragraph(text):
    # 1️⃣ Remove extra spaces
    cleaned_text = ' '.join(text.split())
    # 2️⃣ Convert to Title Case (each word starts with a capital letter)
    title_case_text = cleaned_text.title()

    # 3️⃣ Count vowels (case-insensitive)
    vowels = "aeiou"
    vowel_counts = {vowel: 0 for vowel in vowels}

    for ch in cleaned_text.lower():
        if ch in vowel_counts:
            vowel_counts[ch] += 1

    # 4️⃣ Display results
    print("Processed Text:", title_case_text)
    print("Vowel Counts:")
    for v in vowels:
        print(f"{v.upper()}: {vowel_counts[v]}")


# Main Program
paragraph = input("Enter a paragraph: ")
process_paragraph(paragraph)