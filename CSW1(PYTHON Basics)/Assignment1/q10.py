import string

def count_word_frequency(sentence):
    # 1️⃣ Remove punctuation
    for p in string.punctuation:
        sentence = sentence.replace(p, "")

    # 2️⃣ Convert all to lowercase
    sentence = sentence.lower()

    # 3️⃣ Split sentence into words
    words = sentence.split()

    # 4️⃣ Count word frequencies using a dictionary
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1

    # 5️⃣ Sort words alphabetically
    sorted_words = sorted(word_count.items())

    # 6️⃣ Display results
    print("Word Frequencies:")
    for word, count in sorted_words:
        print(f"{word}: {count}")


# Main Program
sentence = input("Enter a sentence: ")
count_word_frequency(sentence)