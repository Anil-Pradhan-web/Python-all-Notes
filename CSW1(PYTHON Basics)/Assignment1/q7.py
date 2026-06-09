import string
sentence = input("Enter a sentence: ")
separator = input("Enter a custom separator: ")

# Step 2: Remove punctuation marks
for p in string.punctuation:
    sentence = sentence.replace(p, "")

# Step 3: Split sentence into words
words = sentence.split()

# Step 4: Convert all words to lowercase for uniform sorting
words = [word.lower() for word in words]

# Step 5: Sort words in reverse alphabetical order
words.sort(reverse=True)

# Step 6: Join the sorted words using the custom separator
result = separator.join(words)

# Step 7: Display the result
print("\nSorted and Joined Words:")
print(result)
