# Input / Output in Python

## Simple Explanation (Hinglish)
Jab humein user se kuch value leni hoti hai (jaise unka naam ya age), toh hum `input()` ka use karte hain. Aur jab humein screen par kuch dikhana hota hai, toh `print()` ka use karte hain. Samajh lo, `input()` sunne ka kaam karta hai aur `print()` bolne ka.

## Theory (Clear + Structured)
- **Output (`print()`)**: Used to display information on the console. It can take multiple arguments, separated by commas.
- **Input (`input()`)**: Used to take input from the user. By default, `input()` always reads the data as a **String**. If you need an integer or float, you must typecast it.

## Syntax
```python
# For Output
print("Message", variable)

# For Input
variable = input("Prompt message: ")
```

## Examples

```python
# Example 1: Basic Input and Output
name = input("Enter your name: ")
print("Hello", name)

# Example 2: Typecasting Input
age = int(input("Enter your age: "))
years_left = 100 - age
print("You will turn 100 in", years_left, "years.")

# Example 3: F-strings (Modern way to format strings)
city = "Delhi"
print(f"I live in {city}.")
```

## Dry Run / Explanation
* `input("Enter your age: ")`: Yeh user ko prompt show karega aur value enter karne ka wait karega.
* Agar user ne `25` enter kiya, toh woh pehle ek string `"25"` banega.
* `int()` us `"25"` ko integer `25` mein convert karega, kyunki string ke saath math operations (jaise `100 - "25"`) nahi ho sakte.
* F-string (`f"..."`) variables ko directly string ke andar `{}` brackets mein likhne ki facility deta hai. Use f-strings for clean output formatting.

## Common Mistakes
1. **Forgetting to Typecast**: Trying to add numbers from input without converting them (e.g., `num1 + num2` where both are strings will result in concatenation, not mathematical addition).
2. **Missing `f` in F-strings**: Using `{var}` without writing `f` before the string throws no error, but literally `{var}` is printed as it is.

## Interview Notes
1. **Default Type of Input**: Always remember to tell the interviewer that `input()` returns a string by default.
2. **End and Sep parameters in Print**: 
   - `print("A", "B", sep='-')` outputs `A-B`.
   - `print("A", end=' ')` prevents a new line after printing.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Take the user's first name and last name as input and print them together.
2. **(Basic)** Take a number as input and print its square using multiplication.
3. **(Medium)** Write a program to take two numbers as input and print their sum, difference, and product.
4. **(Medium)** Take input of length and breadth of rectangle, calculate area and perimeter.
5. **(Hard)** Format a print statement using `f-strings` to display: "My name is [Name], I am [Age] years old, and my salary is [Salary] LPA." padded with leading zeros for salary.
