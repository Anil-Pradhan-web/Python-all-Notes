try:
    with open("diary.txt", "r") as f:
        print(f.read())
except FileNotFoundError:
    print("File not found. Please check the name.")
