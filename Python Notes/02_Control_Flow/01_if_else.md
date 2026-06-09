# If-Else Conditional Statements

## Simple Explanation (Hinglish)
Life mein hum kaafi decisions lete hain conditions ke base par. Jaise "Agar baarish hui, toh chhatri le jaunga, warna nahi". Code mein yahi logic likhne ke liye hum `if-else` ka use karte hain. Yeh code ko batata hai ki kab kaunsa hissa chalana hai.

## Theory (Clear + Structured)
Conditional statements allow a program to execute certain pieces of code depending on whether a condition is true or false.

- **`if` statement**: Executes if the condition is True.
- **`elif` (else if)**: Used to check multiple conditions sequentially if the previous conditions were False.
- **`else` statement**: Executes when all previous `if`/`elif` conditions are False.

Indentation is highly important in Python to define blocks of code inside these statements.

## Syntax
```python
if condition1:
    # code to execute if condition1 is True
elif condition2:
    # code to execute if condition2 is True
else:
    # code to execute if all conditions are False
```

## Examples

```python
# Example 1: Basic If-Else
marks = 75

if marks >= 90:
    print("Grade: A")
elif marks >= 70:
    print("Grade: B")
elif marks >= 50:
    print("Grade: C")
else:
    print("Grade: F (Fail)")
```

## Dry Run / Explanation
* `marks = 75`. Pehla check `marks >= 90` false hai, toh yeh `if` block skip ho jayega.
* Dusra check `marks >= 70` true ho gaya (`75 >= 70`), toh loop uske andar ghusega aur "Grade: B" print karega.
* Ek baar `True` mil gaya, toh baaki ke `elif` aur `else` block automatically chhod diye jayenge.

## Common Mistakes
1. **IndentationError**: Python uses spaces/tabs to define scope. Forgetting to indent code inside `if` block is a common mistake.
2. **Using `=` instead of `==` in conditions**: Writing `if x = 5:` instead of `if x == 5:`.
3. **Missing Colons**: Forgetting the `:` at the end of `if`, `elif`, or `else` lines.

## Interview Notes
1. **Ternary Operator**: Mention the inline if-else representation which is helpful in making code concise: `result = "Pass" if marks > 50 else "Fail"`
2. Always write conditions from the most restrictive to the least restrictive for logic to work correctly in `if-elif` ladders.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write code to check if a person is eligible to vote (age >= 18).
2. **(Basic)** Write a program to check if a number is even or odd.
3. **(Medium)** Find the largest among three numbers using if-elif-else statements.
4. **(Medium)** Create a grade calculator: A (90-100), B (80-89), C (70-79), D (60-69), F (<60).
5. **(Hard)** Write a calculator program that takes two numbers and an operator (+, -, *, /) as input and returns the result using nested if-else.
