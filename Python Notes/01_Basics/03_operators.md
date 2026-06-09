# Operators in Python

## Simple Explanation (Hinglish)
Operators wo symbols hote hain jo variables aur values par operations (kaam) perform karte hain. Jaise a aur b ko jodna ho toh `+` operator use hota hai. Python mein math, comparison, aur logical kaam karne ke liye alag-alag operators hote hain.

## Theory (Clear + Structured)
Operators are special symbols that carry out arithmetic or logical computation. The value the operator operates on is called the operand.

Types of Operators:
1. **Arithmetic Operators**: Used for mathematical operations (`+`, `-`, `*`, `/`, `//`, `%`, `**`).
2. **Assignment Operators**: Used to assign values to variables (`=`, `+=`, `-=`).
3. **Comparison Operators**: Used to compare two values (`==`, `!=`, `>`, `<`, `>=`, `<=`).
4. **Logical Operators**: Used to combine conditional statements (`and`, `or`, `not`).

## Syntax
```python
result = operand1 operator operand2
```

## Examples

```python
# Arithmetic
a = 10
b = 3
print(a + b)  # Addition: 13
print(a / b)  # Normal Division: 3.333
print(a // b) # Floor Division (removes decimal): 3
print(a % b)  # Modulo (remainder): 1
print(a ** b) # Exponentiation (10 power 3): 1000

# Comparison & Logical
x = 5
print(x > 3 and x < 10)  # True because both conditions are True
print(x == 5)            # True
```

## Dry Run / Explanation
* `a // b`: Division hone ke baad jo decimal part hota hai usko ignore kar deta hai. `10/3 -> 3.33`, but `10//3 -> 3`.
* `a % b`: Modulo operator divide karne ke baad remainder deta hai. `10 % 3` bachega `1`.
* `and` operator tabhi `True` deta hai jab uske dono side ki conditions `True` ho.

## Common Mistakes
1. **Confusing `=` and `==`**: `=` is used to assign a value (e.g., `x = 5`), whereas `==` is used to check equality (e.g., `if x == 5:`).
2. **Using `/` instead of `//`**: Beginners use `/` expecting an integer result, but `/` always returns a float in Python 3.

## Interview Notes
1. Interviewers often ask about the `%` (modulo) operator because it is heavily used in logic building, e.g., checking if a number is even/odd (`number % 2 == 0`).
2. **Short-Circuiting**: In logical `and`, if the first condition is `False`, Python doesn't check the second condition. In logical `or`, if the first is `True`, it doesn't check the second.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a program to check if a number is even or odd using the `%` operator.
2. **(Basic)** Use floor division `//` to find how many times 3 fits in 20.
3. **(Medium)** Given a 3-digit number, use `//` and `%` to extract and print its last digit.
4. **(Medium)** Check if a number lies between 10 and 100 using comparison and logical operators.
5. **(Hard)** Write a logical expression that evaluates to `True` if a variable `year` is a leap year.
