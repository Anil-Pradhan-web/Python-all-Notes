# String Deep Dive

## Simple Explanation (Hinglish)
Python mein strings par kaam karna bohot simple aur mazedar hai. String sirf text hoti hai (letters mili hui list ki tarah). Python humein bohot saare methods deta hai text ko format karne, todne (split), jodna (join), aur slice karne ke liye.

## Theory (Clear + Structured)
Strings in Python are immutable arrays of characters. 
- **Immutability**: Once a string object is created, you cannot change its specific characters.
- **Slicing**: You can extract a part of a string using `[start : stop : step]`.
- **Useful Methods**: `upper()`, `lower()`, `strip()`, `split()`, `join()`, `replace()`.

## Syntax
```python
my_string = "Hello World"
slice = my_string[start_index:end_index]
```

## Examples

```python
# Example 1: Basic String Methods
text = "   Python is fun!   "
print(text.strip())           # Removes leading/trailing whitespaces
print(text.lower())           # Converts to lowercase
print(text.replace("fun", "easy")) # Replaces a substring

# Example 2: Split and Join
sentence = "I love coding"
words = sentence.split()      # Splits by spaces -> ['I', 'love', 'coding']
print(words)

new_sentence = "-".join(words) # Joins list with hyphens
print(new_sentence)           # Output: I-love-coding

# Example 3: Slicing
word = "DEVELOPER"
print(word[0:3])   # DEV (from index 0 to 2)
print(word[::-1])  # REPOLEVED (Reverses the string!)
```

## Dry Run / Explanation
* `split()`: Default roop se spaces par string ko todta hai aur list return karta hai.
* `"-".join(words)`: Us list ke har item ke beech mein `-` daal kar wapas ek new string bana deta hai.
* `[::-1]`: Slicing ka advanced concept. Start aur stop humne khali chhod diya isliye puri string lega, par step `-1` diya toh string ko peeche se reverse read karega.

## Common Mistakes
1. Trying to change a character: `string[0] = 'a'` throws a `TypeError`. You must create a new string.
2. Mixing up `split` and `join` object types: `join` is called *on* the separator string, passing the list as argument (`",".join(list)`).

## Interview Notes
1. **String Reversal**: `string[::-1]` is the fastest and most pythonic way to reverse a string. Interviewers explicitly ask this!
2. **Palindrome Check**: Easy one-liner: `is_palindrome = word == word[::-1]`.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Reverse a string using slicing [::-1].
2. **(Basic)** Check if a string is palindrome using string reversal.
3. **(Medium)** Check if two strings are anagrams of each other.
4. **(Medium)** Find longest word in a sentence.
5. **(Hard)** Write a program that converts a snake_case string (e.g., `my_variable_name`) to camelCase (`myVariableName`).
