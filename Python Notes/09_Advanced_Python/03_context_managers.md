# Context Managers (`with` statement)

## Simple Explanation (Hinglish)
Kabhi kisi hotel ka room book kiya hai? Rule hota hai: Checking-in karo room milta hai (Entry), apna use karo, aur nikalne se pehle cheezein properly lock ya Check-out karke aao (Exit). 
Code mein waise hi database ya files kholte waqt bhool na jaye 'Check-out' karna, uske liye **Context Managers** use hote hain. `with` keyword jo aage piche automatically check-in aur check-out handle kar leta hai.

## Theory (Clear + Structured)
A **Context Manager** allows you to allocate and release resources exactly when you want to. It gracefully handles the setup and teardown phases of resource management, even if errors occur in between.
The most widely used example of a context manager is the `with` statement.
To build a custom context manager, a class must implement the Dunder methods:
- `__enter__()`: Sets up the resource.
- `__exit__()`: Tears down the resource.

## Syntax
```python
with context_manager() as variable:
    # use variable
# automatically closed/cleaned up here
```

## Examples

```python
# Example 1: The standard file Context Manager
with open("some_file.txt", "w") as f:
    f.write("We don't need to write f.close() !")
# f is automatically closed outside the block

# Example 2: Creating your own Context Manager
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        
    def __enter__(self):
        print("Checking IN - Opening file")
        self.file = open(self.filename, self.mode)
        return self.file # This is assigned to the 'as' variable
        
    def __exit__(self, exc_type, exc_val, traceback):
        print("Checking OUT - Closing file safely")
        self.file.close()

# Using the custom context manager
with FileManager("test.txt", "w") as my_file:
    print("Writing data...")
    my_file.write("Learning Context Managers.")
```

## Dry Run / Explanation
* Job log line `with FileManager("test.txt", "w") as my_file:` aayegi..
* Internally, Python sabse pehle `__enter__` method call karega. Us method ne sach mein file ko `open` kiya aur return kardi apni value jo `my_file` mei save hogayi.
* Ab humne block ke andar print aur write wale operation kare.
* Jaise hi wo block end pe aya, Python explicitly automatically `__exit__` function ko call karega jo dhyaan rakhte hue `self.file.close()` chala dega. Chahe aapke andar wale block mein error / exception hi kyon naa aya ho, exit execute nischit hoti hai.

## Common Mistakes
1. Creating a custom database connection class but forgetting that `__enter__` must return the connection object so that it can be used within the `with` block (accessed via `as connection`).
2. Not accounting for the extra parameters `exc_type`, `exc_val`, `traceback` inside `__exit__`. These are mandatory because Python passes exception details into `__exit__` if the block crashed.

## Interview Notes
1. Can we write custom context managers as functions instead of classes? Yes! Python's `contextlib` module gives us a decorator `@contextmanager` which makes this possible using generator behavior (`yield`).
2. Primary advantage: Ensures resource teardown safely preventing memory leaks and database deadlocks.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** List 3 scenarios (other than files) where context managers are extremely useful.
2. **(Basic)** Write a simple `with` statement to open a file and write a line, demonstrating automatic closing.
3. **(Medium)** Use the `sqlite3` module and document how using `with sqlite3.connect(...)` saves you from forgetting to close the DB.
4. **(Medium)** Create a custom context manager using `@contextmanager` decorator from `contextlib` module.
5. **(Hard)** Write a custom context manager called `Timer` that calculates how long the code inside the `with` block took to run, and prints it during `__exit__`.
