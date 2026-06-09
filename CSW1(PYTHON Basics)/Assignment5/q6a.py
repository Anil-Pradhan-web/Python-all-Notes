import os
from datetime import date

if os.path.exists("diary.txt"):
    print("File already exists.")
else:
    note = input("Enter diary note: ")
    with open("diary.txt", "w") as f:
        f.write(str(date.today()) + "\n")
        f.write(note)
    print("Diary saved successfully.")
