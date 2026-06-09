# Loops (For and While)

## Simple Explanation (Hinglish)
Kabhi kabhi humein ek hi kaam baar-baar karna padta hai, jaise apna naam 100 baar print karna. Iske liye 100 lines ka `print()` likhna bewakoofi hai. Loops isi kaam aate hain. Yeh ek code block ko tab tak repeat karte hain jab tak condition meet hoti hai.

## Theory (Clear + Structured)
Loops are used to execute a block of code repeatedly.

1. **`for` loop**: Used when the number of iterations is known before entering the loop. It iterates over a sequence (like a list, tuple, string, or range).
2. **`while` loop**: Used when the number of iterations is unknown, and it depends on a condition. It repeats block of code as long as the condition is `True`.

## Syntax
```python
# For Loop
for item in sequence:
    # code

# While Loop
while condition:
    # code
```

## Examples

```python
# Example 1: For loop with range()
# Prints 0 to 4
for i in range(5):
    print("For loop iteration:", i)

# Example 2: Iterating over a string
name = "Python"
for char in name:
    print(char)

# Example 3: While loop
count = 3
while count > 0:
    print("While count is:", count)
    count -= 1  # Important to avoid infinite loop
```

## Dry Run / Explanation
* `range(5)` basically 0 se lekar 4 tak numbers generate karta hai. `i` ki value pehle 0 hogi, print karega, fir 1 hogi... aese karte 4 tak jayega.
* `while count > 0`: Pehle `count` 3 hai (3>0 true hai), print hua, fir `count` 2 ho gaya (`count -= 1`). Aese jab `count` 0 hoga, condition false jayegi aur loop ruk jayega.

## Common Mistakes
1. **Infinite Loops**: Forgetting to update the variable inside a `while` loop (like `count -= 1`) creates an infinite loop that crashes the program.
2. **Off-by-One Error**: `range(1, 10)` generates numbers from 1 to 9, not 10. Beginners often assume it includes the upper limit.

## Interview Notes
1. **`else` with loops**: Python has a unique feature where `else` can be tied to a loop. The `else` block runs only if the loop finishes successfully without encountering a `break` statement.
2. `for` loops are generally faster and safer than `while` loops when iterating over sequences.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Print all even numbers from 1 to 20 using for loop.
2. **(Basic)** Print multiplication table of 5 using for loop.
3. **(Medium)** Find sum of all digits of a number using while loop.
4. **(Medium)** Check if a number is prime using for loop.
5. **(Hard)** Print a pattern of stars using nested loops:
