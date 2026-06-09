try:
    with open("data.txt", "r") as f:
        print("File opened successfully.")
        print("Contents of data.txt:")
        print(f.read())
except FileNotFoundError:
    print("Error: File not found.")
