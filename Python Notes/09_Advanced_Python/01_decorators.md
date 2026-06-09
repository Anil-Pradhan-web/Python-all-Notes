# Decorators

## Simple Explanation (Hinglish)
Agar mere paas koi function hai (jaise burger ki tikki), aur main chahta hoon ki original function ke code ko bina change kiye, uske aage-peeche kuch code (jaise bun, cheese, sauce) lag jaye, toh main **Decorators** use karuga. Yeh kisi bhi function ke nature ko 'decorate' ya enhance kar dete hain bina uska original source code edit kiye.

## Theory (Clear + Structured)
A **Decorator** is a function that takes another function as an argument, extends or modifies its behavior, and returns a new function.
They rely on the concept of **Higher-Order Functions** and **Closures**. In Python, they are applied using the `@decorator_name` syntax above a function definition.

Prerequisites to understanding decorators:
1. In Python, functions are first-class citizens (they can be passed as variables).
2. A function can be defined inside another function.

## Syntax
```python
@decorator_name
def normal_function():
    pass
```

## Examples

```python
# Step 1: Defining a Decorator
def my_custom_decorator(func):
    def wrapper():
        print("Function run hone se *pehle* yeh print hoga.")
        func()  # Calling the original function inside the wrapper
        print("Function run hone ke *baad* yeh print hoga.")
    return wrapper

# Step 2: Applying the Decorator
@my_custom_decorator
def say_hello():
    print("Hello Friends!")

# Step 3: Calling the decorated function
say_hello()
```
**Output:**
```text
Function run hone se *pehle* yeh print hoga.
Hello Friends!
Function run hone ke *baad* yeh print hoga.
```

## Dry Run / Explanation
* `def my_custom_decorator(func)`: Yeh function input me ek aur function le raha hai (`say_hello` ban gaya `func`).
* `@my_custom_decorator` lagane se: Python check karega kaunsa decorator hai, us decorator ko call karega, aur uske andar original function ko bhij jayega. 
* Final call mein sach mein chalne wali cheez `wrapper()` function hai, jiske beech mein humara aukaat me original `say_hello` function chalta hai.

## Common Mistakes
1. Forgetting to `return wrapper` at the end of the decorator function. Without returning it, the decorated function becomes `None`.
2. Dealing with arguments: If `say_hello(name)` required arguments, the inner `wrapper` must also be defined to accept them like `def wrapper(*args, **kwargs):` and pass them to `func(*args, **kwargs)`.

## Interview Notes
1. **Real-World Usage**: Decorators are heavily used in frameworks like Flask/Django for Routing (`@app.route()`), Login checks (`@login_required`), or measuring performance (`@time_it`).
2. Be prepared to explain how to write a decorator that accepts arguments for a target function. (Answer: Use `*args, **kwargs` inside the wrapper function).

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a simple decorator that just prints "Executing..." before calling a target function.
2. **(Basic)** Write a decorator that prints "Start" before a function call and "End" after it.
3. **(Medium)** Write a decorator that takes a function and runs it twice sequentially.
4. **(Medium)** Create a decorator that wraps arguments and keyword arguments and logs them along with the function name.
5. **(Hard)** Create a `@time_it` decorator using the `time` module that calculates and prints the exact time a function took to execute. Apply it to a function containing a `for` loop of 1,000,000 iterations.
