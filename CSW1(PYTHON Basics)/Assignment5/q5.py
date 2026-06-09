with open("poem.txt", "r") as f:
    first_ten = f.read(10)
    print("First 10 characters:", first_ten)

    f.seek(0)
    print("Full file contents after seek():")
    print(f.read())
