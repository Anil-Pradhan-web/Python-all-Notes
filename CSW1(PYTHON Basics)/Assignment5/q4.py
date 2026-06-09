with open("poem.txt", "r") as f:
    lines = f.readlines()

num_lines = len(lines)
num_words = sum(len(line.split()) for line in lines)
num_chars = sum(len(line) for line in lines)

print("Number of lines:", num_lines)
print("Number of words:", num_words)
print("Number of characters:", num_chars)
