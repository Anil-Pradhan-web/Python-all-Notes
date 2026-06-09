# Variables and Data Types

## Simple Explanation (Hinglish)
Variables programming mein "containers" ki tarah hote hain jahan hum data store karte hain. Jaise ghar mein chini (sugar) rakhne ke liye ek dabba hota hai, wese hi data ko rakhne ke liye variable ka use hota hai. Python mein variable banana bohot simple hai, aapko type batane ki zaroorat nahi hoti (kyunki Python dynamically typed hai).

## Theory (Clear + Structured)
A **variable** is a named location in memory used to store data. In Python, you don't need to declare the variable type explicitly. 

**Data Types** define the type of data a variable holds. Common data types in Python include:
- **Integer (`int`)**: Whole numbers (e.g., 5, -10)
- **Float (`float`)**: Decimal numbers (e.g., 3.14, -0.5)
- **String (`str`)**: Text data enclosed in quotes (e.g., "Hello", 'Python')
- **Boolean (`bool`)**: Represents `True` or `False`

## Syntax
```python
variable_name = value
```

## Examples

```python
# Example 1: Basic Variables
age = 20          # int
price = 99.99     # float
name = "Rahul"    # str
is_student = True # bool

print(name)
print(age)

# Example 2: Multiple Assignments
a, b, c = 1, 2, "Hello"
print(a, b, c)

# Example 3: Checking type
print(type(price)) # class <'float'>
```

## Dry Run / Explanation
* `age = 20`: Yahan humne `age` naam ka ek variable banaya aur usme `20` assign kiya. Python automatically samajh gaya ki yeh integer hai.
* `print(name)`: `name` variable ki value console mein dikha dega.
* `type()`: Ek in-built function hai jo batata hai variable mein kis tarah ka data rakha hai.

## Common Mistakes
1. **Naming Variables Incorrectly**: Variable names cannot start with a number (e.g., `1name = "Rahul"` will throw an error).
2. **Case Sensitivity**: `Age` and `age` are two different variables. Beginners often confuse them.
3. **Forgetting Quotes for Strings**: Writing `name = Rahul` instead of `name = "Rahul"` will cause a `NameError`.

## Interview Notes
1. **Dynamic Typing**: Interviewer might ask "Why is Python called dynamically typed?". Answer: Because we don't need to declare the data type explicitly. The interpreter infers it at runtime.
2. **Immutability**: Strings and integers are immutable in Python. Changing a string creates a new object in memory.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Create a variable `city` and assign your city name to it. Print the variable.
2. **(Basic)** Find the data type of the value `3.14159` using a built-in function.
3. **(Medium)** Swap the values of two variables `a = 10` and `b = 20` without using a third variable.
4. **(Medium)** Create two variables `num1 = "100"` and `num2 = "200"` (as strings). Add them after converting to integers.
5. **(Hard)** Create a temperature converter: Take Celsius as input and convert to Fahrenheit using formula `F = C * 9/5 + 32`.
