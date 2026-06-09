# Modules and Packages

## Simple Explanation (Hinglish)
Jab code bohot bada ho jata hai, toh hum saara code ek hi dookaan (file) mein nahi rakhte. Hum alag-alag departments (files) bana dete hain. In alag files ko **Modules** bolte hain. 
Aur jab bahot saare modules ko ek properly organized folder mein dalte hain, toh us folder ko **Package** bolte hain. Kisi dusri file se variables ya functions mangwane ke liye hum `import` ka use karte hain.

## Theory (Clear + Structured)
- **Module**: A simple `.py` file containing Python code (functions, classes, variables).
- **Package**: A directory that contains a collection of modules. It usually includes a special file called `__init__.py` (required in older Python versions) which tells Python that this directory is a package.
- **Import Statements**: Used to bring code from one module into another.

## Syntax
```python
import module_name
from module_name import function_name
```

## Examples

```python
# Assuming we have a file named "math_ops.py" with a function add(a, b):

# Example 1: Basic Import
import math_ops

result = math_ops.add(5, 10)
print(result)

# Example 2: Importing specific function
from math_ops import add

result = add(5, 10)  # Direct use without module name prefix
print(result)

# Example 3: Aliasing (Giving a nickname)
import math_ops as m

print(m.add(5, 10))
```

## Dry Run / Explanation
* `import math_ops`: Python dekhega ki kya `math_ops.py` naam ki koi file aas-paas (ya library path mein) hai? Agar hai toh usko load kar lega. Usko use krne k liye module ka naam dot `.` lagana padta hai (`math_ops.add()`).
* `from math_ops import add`: Is syntax se aap seedha function utha lete ho. Fayda yeh hai ki baar baar `math_ops.` likhne ki mehnat nahi lagti.

## Common Mistakes
1.  **Circular Imports**: File A imports File B, and File B imports File A. This causes Python to crash with a confusing Import error.
2.  **Naming conflicts**: Naming your python file the same as a built-in module (e.g., naming your file `random.py` will break Python's actual `random` library if you try to import it).

## Interview Notes
1. **`__main__` block**: Interviewers often ask about `if __name__ == "__main__":`. It is used to ensure that a piece of code runs ONLY if the file is run directly, and NOT if it is imported into another file.
2. What does `__init__.py` do? It treats the directory as a package and allows you to run initialization code.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Import Python's built-in `math` module and use it to print the square root of 16.
2. **(Basic)** Use `from random import randint` to generate random number between 1-100.
3. **(Medium)** Create a file `greetings.py` with a function `say_hello()`. Create a second file `main.py` and import that function from the first file.
4. **(Medium)** Use `if __name__ == "__main__":` to make module executable and importable.
5. **(Hard)** Explain practically how `if __name__ == "__main__":` prevents code from executing during an import by making two files and demonstrating it.
