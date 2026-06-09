text = "Python"

with open("strings.txt", "wb") as f:
    f.write(text.ljust(20).encode())
    f.write(text.encode())

print("Fixed length storage:", repr(text.ljust(20)))
print("Variable length storage:", repr(text))
