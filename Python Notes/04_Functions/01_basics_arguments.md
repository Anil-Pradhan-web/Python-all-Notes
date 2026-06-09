# Functions and Arguments

## Simple Explanation (Hinglish)
Maan lo aapko har roj chai banani padti hai. Step wahi hotay hain (paani dalo, patti dalo, ubaalo...). Agar is kaam ko ek baar ek 'machine' mein feed kar do, toh baad mein bus button (call) dabana padega. Is 'machine' ko coding mein Function kehte hain. 
Arguments ya Parameters kya hote hain? Jo cheez aap machine mein alag se daloge, jaise sugar kitni dalni hai, woh argument hota hai.

## Theory (Clear + Structured)
A function is a block of reusable code that only runs when it is called.
- `def` keyword: Used to define a function.
- **Parameters**: Variables defined in the function signature.
- **Arguments**: Actual values passed to the function when calling.
- **Return Statement**: Sends a value back to the caller and exits the function.

## Syntax
```python
def function_name(parameter1, parameter2):
    # code logic
    return result
```

## Examples

```python
# Example 1: Simple Function Default argument
def greet(name="User"):
    print(f"Hello, {name}!")

greet("Aman") # Output: Hello, Aman!
greet()       # Output: Hello, User!

# Example 2: Return function
def add_numbers(num1, num2):
    ans = num1 + num2
    return ans

result = add_numbers(10, 20)
print(result) # Output: 30

# Example 3: Variable Length Arguments (*args and **kwargs)
def print_hobbies(*args):
    # args behaves like a tuple
    for hobby in args:
        print(hobby)

print_hobbies("Cricket", "Music", "Coding")
```

## Dry Run / Explanation
* `def greet(name="User")`: Yahan `name` ka default value `User` diya hai. Matlab jab function call karte waqt parameter nahi denge (jaise `greet()`), tab `name` automatically `User` ban jayega.
* `return ans`: `print` aur `return` alag hote hain. Print bus console pe dikhata hai, lekin jabki Return real value lauta k deta hai jo kisi loop/calc mein further use ho sakti hai (jaise `result` variable mein store karna).
* `*args`: Agar pata na ho kitne inputs aane wale hain, toh `*args` use karte hain jo saare inputs ko combine array/tuple bana leta hai.

## Common Mistakes
1. Not returning a value from a function. Default return is `None`. If you try `ans = greet("Alia")` without return, `ans` will be `None`.
2. Positional argument after keyword argument error (e.g., `func(x=5, 10)` is wrong, `func(10, x=5)` is fine).

## Interview Notes
1. **Pass by Object Reference**: Python handles variables by object reference, which means mutable objects (lists/dicts) passed into a function can be modified inside the function globally.
2. Interviwer might ask difference between `*args` and `**kwargs`. `*args` receives a tuple of positional arguments, `**kwargs` receives a dictionary of keyword arguments.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a function `square(number)` that returns the square of the number.
2. **(Basic)** Write function to calculate area of rectangle (length * breadth).
3. **(Medium)** Write function that accepts variable arguments (*args) and returns their sum.
4. **(Medium)** Create function that takes dictionary (**kwargs) and prints key-value pairs.
5. **(Hard)** Create function with mutable default argument trap demonstration.
