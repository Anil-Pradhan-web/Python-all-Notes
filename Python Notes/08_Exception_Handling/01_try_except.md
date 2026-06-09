# Exception Handling

## Simple Explanation (Hinglish)
Kabhi-kabhi aapka logic bilkul sahi hota hai code mein, par bahar ke reasons se code fatega. Jaise aap net se video download kar rahe ho aur beech mein wifi band ho gaya. Aise waqt par Python gussa hoke poora program crash kar dega ("Error aagya!").
Crash roknay ke liye hum `try-except` ka dhaal (shield) use karte hain. "Bhai ye `try` karle, agar phata toh crash mat kar, `except` block ko chalakar aaram se bata dena ki problem aayi hai."

## Theory (Clear + Structured)
An **Exception** is an event that occurs during the execution of a program that disrupts the normal flow of instructions.
To handle these exceptions gracefully without crashing, we use:
- **`try`**: Block of code where you expect an error may happen.
- **`except`**: Block of code that runs ONLY if an error occurs in the `try` block.
- **`else`**: Runs ONLY if the `try` block succeeded without any errors.
- **`finally`**: Runs NO MATTER WHAT (success or failure). Usually used for cleanup (like closing files/connections).

## Syntax
```python
try:
    # Risky code
except ExceptionType:
    # Error handling code
finally:
    # Cleanup code
```

## Examples

```python
# Example 1: Basic Try-Except
try:
    num = int(input("Enter a number: "))
    ans = 10 / num
    print(ans)
except ZeroDivisionError:
    print("Bhai, zero se divide nahi kar sakte!")
except ValueError:
    print("Sirf numbers dalo, letters nahi!")

# Example 2: Finally & Else Blocks
try:
    file = open("test.txt", "r")
    data = file.read()
except FileNotFoundError:
    print("File to mili hi nahi yaar.")
else:
    print("File mil gayi aur error bhi nahi aaya.")
finally:
    print("Main to har haal mein run hounga!")
```

## Dry Run / Explanation
* `try:` code input mangega. Jo agar user ne normal number (e.g. `2`) dala, to `10/2` = `5` print hoga. Code `except` blocks ko ignore kar dega (kyunki error aaya hi nahi).
* Par maan lo user ne `0` daala. `10/0` math mein invalid hai. Python ko crash hona tha (ZeroDivisionError), par kyunki wo `try` ke andar tha, wo sidhe `except ZeroDivisionError:` waale block par jump karega aur gracefully message dega.
* `finally:` ka message 100% chalega (chahe error aayi ho ya nahi).

## Common Mistakes
1. Using a naked `except:` without specifying the error type. This acts like a black hole and hides ALL errors (even syntax or keyboardInterrupts), making debugging a nightmare. Always specify the error or at least use `except Exception as e:`.
2. Putting too much code inside the `try` block. Only put the specific line that might cause an error in the `try` block.

## Interview Notes
1. **Raising Exception**: You can manually trigger an error using the `raise` keyword (e.g., `raise ValueError("Invalid age")`).
2. Why use `finally`? Interviewer asks "If except handles it, why need finally?". Answer: Even if except fails to catch an error and the program is about to crash, `finally` will STILL execute, ensuring things like database connections are safely closed.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a `try-except` block to handle an `IndexError` when trying to access `list[10]` in a list of 3 items.
2. **(Basic)** Write a program to handle `ZeroDivisionError` when dividing two numbers.
3. **(Medium)** Ask the user for two integers and print their sum. Use exception handling to keep asking if the user enters a string instead of an int.
4. **(Medium)** Write a program that handles multiple exceptions (`ValueError` and `ZeroDivisionError`) in a single try-except structure.
5. **(Hard)** Write a custom function to validate an age input. Raise a `ValueError` if the age is negative, and handle it gracefully.
