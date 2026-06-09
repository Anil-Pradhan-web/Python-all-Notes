# File Handling

## Simple Explanation (Hinglish)
Aapka text variables ya lists mein jo bhi result store hota hai, program band hote hi delete ho jata hai (kyunki RAM clean ho jati hai). Agar us data ko parmanent save karna hai hard drive pe, toh usay Files mein likhna padta hai. Python files ko open, read, write aur close karne ke asaan tarike deta hai.

## Theory (Clear + Structured)
File handling in Python implies working with files on the disk.
The main operations are:
- **`open()`**: Opens a file and returns a file object.
- **Modes**:
  - `'r'`: Read (default). Fails if the file does not exist.
  - `'w'`: Write. Overwrites if file exists, creates if it doesn't.
  - `'a'`: Append. Writes to the end of the file. Creates if it doesn't exist.
- **`read()` / `readlines()`**: To read data from the file.
- **`write()` / `writelines()`**: To write data to the file.
- **`close()`**: Saves the file and releases memory.

## Syntax
```python
file = open("filename.txt", "mode")
data = file.read()
file.close()

# Better syntax using 'with'
with open("filename.txt", "mode") as file:
    # file operations here
```

## Examples

```python
# Example 1: Writing to a file (Overwrites existing data)
with open("data.txt", "w") as file:
    file.write("Hello World!\n")
    file.write("Python is awesome.")

# Example 2: Appending to a file (Adds to existing data)
with open("data.txt", "a") as file:
    file.write("\nLearning File Handling.")

# Example 3: Reading a file
with open("data.txt", "r") as file:
    content = file.read()
    print("File Content:")
    print(content)
```

## Dry Run / Explanation
* `open("data.txt", "w")`: Python disk par "data.txt" file check karega. Agar nahi mili, toh wo nayi file bana dega. Phir usmein `"Hello World"` chipka dega.
* `with open() as file`: Yeh `with` statement bahut accha syntax hai. Jaise hi `with` ka block (indentation) khatam hota hai, file automatically `file.close()` ho jati hai! Humein bhoolne ka dar nahi rehta.
* `file.read()`: Puri file ko ek badi string ke roop mein variable (`content`) mein dal dega.

## Common Mistakes
1. Opening a file in `'w'` (write) mode when you just want to add a line. Write mode deletes the old content immediately! Use `'a'` (append).
2. Forgetting to `.close()` the file. If not closed, changes might not physically save to the disk properly. (This is why the `with` block is preferred).

## Interview Notes
1. **`read()` vs `readlines()`**: `read()` loads the whole file as one single String. `readlines()` returns a List of strings, where each element is a line. Which is better? If the file is huge (like 2GB logs), `read()` will crash your RAM. Use `for line in file:` instead.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a program to create a file named `my_name.txt` and write your full name inside it.
2. **(Basic)** Create a file, write three lines of text, then read and print the entire file content.
3. **(Medium)** Open a text file, count the total number of lines inside it, and print the count.
4. **(Medium)** Read a text file and copy its contents into a new file, but in uppercase.
5. **(Hard)** Write a program that asks the user for logs (input) inside a loop and appends it to `log.txt`. The loop should stop when the user types 'exit'.
