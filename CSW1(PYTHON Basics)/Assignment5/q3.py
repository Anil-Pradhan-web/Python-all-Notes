poem = [
    "Roses are red,\n",
    "Violets are blue,\n",
    "Python is fun,\n",
    "And so are you.\n"
]

with open("poem.txt", "w") as f:
    f.writelines(poem)

print("Poem written to file successfully.")

with open("poem.txt", "r") as f:
    for line in f:
        print(line, end="")
