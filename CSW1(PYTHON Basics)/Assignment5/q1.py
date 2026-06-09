students=["Alice", "Bob", "Charlie", "David", "Eva"]
with open("students.txt", "w") as f:
    for name in students:
        f.write(name + "\n")
print("Student names have been written to students.txt")
with open("students.txt", "r") as f:
    content = f.read()
    print("Contents of students.txt:")
    print(content)