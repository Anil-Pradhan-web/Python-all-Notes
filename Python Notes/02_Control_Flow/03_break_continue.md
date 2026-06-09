# Break, Continue, and Pass

## Simple Explanation (Hinglish)
Maan lo aap ek long journey pe ho (loop). 
- `break`: Achanak car kharab ho gayi, aap journey wahi rok dete ho (loop khatam). 
- `continue`: Raste mein gadha aa gaya, aap us gadhe ko chhod kar aage thoda jump kar lete ho, par journey chalu rehti hai.
- `pass`: Yeh bass ek placeholder hai. Agar aapko lagta hai baad mein kuch likhoge, to waha `pass` daal do warna error aayegi.

## Theory (Clear + Structured)
Loop control statements change execution from its normal sequence. 

- **`break`**: Terminates the loop entirely and transfers execution to the statement immediately following the loop.
- **`continue`**: Skips the rest of the code inside the current iteration and jumps back to the top to check the condition for the next iteration.
- **`pass`**: A null operation. Nothing happens when it is executed. It's used as a placeholder when a statement is syntactically required but you have no code to execute yet.

## Syntax
```python
for item in sequence:
    if condition:
        break     # or continue, or pass
```

## Examples

```python
# Example 1: Break
for i in range(1, 10):
    if i == 5:
        break
    print(i) # Output: 1 2 3 4
print("Loop exited")

# Example 2: Continue
for i in range(1, 6):
    if i == 3:
        continue
    print(i) # Output: 1 2 4 5

# Example 3: Pass
for i in range(5):
    pass     # Will write logic here later
```

## Dry Run / Explanation
* **Break Example**: Loop 1 se 9 tak chalna chahiye tha. Par jab `i` ki value 5 hoti hai, `break` run ho jata hai. Loop wahi turant band ho jata hai aur aage ka print nahi chalta.
* **Continue Example**: Jab `i == 3` hua, `continue` run hua. Usne print ko skip kar diya aur wapas upar loop mein chala gaya next value (4) lekar. Isliye 3 print nahi hua.

## Common Mistakes
1. Placing `break` or `continue` outside a loop. They ONLY work inside `for` or `while` loops.
2. In while loops, using `continue` before updating the increment variable can cause an infinite loop because the update step gets skipped.

## Interview Notes
1. Understand the exact difference: `break` exits the whole loop, while `continue` only jumps to the next iteration.
2. Be prepared to dry-run logic featuring loops combined with `break`.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a loop from 1 to 10 but break the loop if the number is 7.
2. **(Basic)** Print numbers 1 to 15, skip number 8 using continue.
3. **(Medium)** Find first prime number greater than 50 using break and continue.
4. **(Medium)** Search for a number in list, print position and break when found.
5. **(Hard)** Write a program to find the first number divisible by 7 and 11 between 100 and 500, and immediately stop searching once found.
