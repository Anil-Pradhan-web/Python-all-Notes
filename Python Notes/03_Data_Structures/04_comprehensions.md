# Comprehensions (List, Dict, Set) — Ek Line Mein Magic

## Simple Explanation (Hinglish)
Maan lo tumhare paas ek list hai numbers ki, aur tum har number ka double nayi list mein daalna chahte ho. Normal loop se 3-4 lines lagenge:
```python
new_list = []
for x in [1,2,3,4,5]:
    new_list.append(x*2)
```

**Comprehension** se yeh **1 line** mein ho jayega:
```python
new_list = [x*2 for x in [1,2,3,4,5]]
```

Comprehension ek **smart shortcut** hai — loop chalao, condition lagao, aur result immediately list/dict/set mein daalo — **sab ek hi line mein**. Yeh code ko shorter, cleaner aur faster banata hai.

## Theory (Clear + Structured)
Comprehensions provide a **concise way** to create sequences (List, Dictionary, Set) by iterating over an iterable.

- **List Comprehension**: `[expression for item in iterable if condition]`
- **Dict Comprehension**: `{key_expression: value_expression for item in iterable if condition}`
- **Set Comprehension**: `{expression for item in iterable if condition}`
- **Generator Expression**: `(expression for item in iterable if condition)` — parentheses wala, memory-efficient

### Three Parts of Comprehension
1. **Expression**: Kya generate karna hai (jo result chahiye)
2. **Iteration**: Kahan se items aa rahe hain (for loop part)
3. **Condition** (optional): Filter kaunsa item include karna hai (if part)

## Syntax
```python
# List Comprehension
[expression for variable in iterable if condition]

# Dictionary Comprehension
{key: value for variable in iterable if condition}

# Set Comprehension
{expression for variable in iterable if condition}

# Generator Expression (memory efficient)
(expression for variable in iterable if condition)
```

## Examples

### 1. List Comprehension — Basic

```python
# Normal loop se
squares_normal = []
for i in range(1, 6):
    squares_normal.append(i**2)
print(squares_normal)  # [1, 4, 9, 16, 25]

# Comprehension se (1 line)
squares = [i**2 for i in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]
```

### 2. List Comprehension with Condition

```python
# Sirf even numbers ke squares
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_squares = [n**2 for n in numbers if n % 2 == 0]
print(even_squares)  # [4, 16, 36, 64]

# if-else ke saath (condition expression)
# Agar even hai toh square, warna cube
result = [n**2 if n % 2 == 0 else n**3 for n in range(1, 6)]
print(result)  # [1, 4, 27, 16, 125]
```

### 3. Nested Loops in Comprehension

```python
# Flat list from nested loop
pairs = [(x, y) for x in range(3) for y in range(3)]
print(pairs)
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# Matrix flatten karna
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 4. Dictionary Comprehension

```python
# Word ki length ka dictionary
words = ["apple", "banana", "cherry", "date"]
word_lengths = {word: len(word) for word in words}
print(word_lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6, 'date': 4}

# Square numbers ka dict
squares_dict = {x: x**2 for x in range(1, 6)}
print(squares_dict)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {value: key for key, value in original.items()}
print(swapped)  # {1: 'a', 2: 'b', 3: 'c'}

# Condition ke saath
even_squares_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares_dict)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

### 5. Set Comprehension

```python
# Duplicates automatically remove hote hain
numbers = [1, 2, 2, 3, 4, 4, 5, 5, 5]
unique_squares = {x**2 for x in numbers}
print(unique_squares)  # {1, 4, 9, 16, 25}

# Vowels filter karna from string
text = "hello world"
vowels_set = {char for char in text if char in "aeiou"}
print(vowels_set)  # {'o', 'e'} — order guarantee nahi hai set mein
```

### 6. Generator Expression (Memory Efficient)

```python
# List comprehension — pura list memory mein load hota hai
big_list = [x**2 for x in range(1000000)]  # 8 MB memory lega

# Generator — on-the-fly generate karta hai, memory nahi leta
big_gen = (x**2 for x in range(1000000))   # ~200 bytes memory

# Generator ko iterate karo
for val in big_gen:
    if val > 100:
        break
    print(val)

# Generator ko list mein convert kar sakte ho
gen = (x*2 for x in [1, 2, 3])
print(list(gen))  # [2, 4, 6]
```

### 7. Nested List Comprehension (Matrix Operations)

```python
# Identity matrix banana (3x3)
identity = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
print(identity)
# [[1, 0, 0],
#  [0, 1, 0],
#  [0, 0, 1]]

# Matrix transpose karna
matrix = [[1, 2, 3], [4, 5, 6]]
transpose = [[row[i] for row in matrix] for i in range(3)]
print(transpose)  # [[1, 4], [2, 5], [3, 6]]
```

## Dry Run / Explanation

Chalo `even_squares = [n**2 for n in range(1, 9) if n % 2 == 0]` ko step-by-step samajhte hain:

```
range(1, 9) = [1, 2, 3, 4, 5, 6, 7, 8]

Step 1: n = 1  → condition check: 1%2 == 0? → False → skip
Step 2: n = 2  → condition check: 2%2 == 0? → True  → expression: 2**2 = 4 → list mein add
Step 3: n = 3  → condition check: 3%2 == 0? → False → skip
Step 4: n = 4  → condition check: 4%2 == 0? → True  → expression: 4**2 = 16 → list mein add
Step 5: n = 5  → condition check: 5%2 == 0? → False → skip
Step 6: n = 6  → condition check: 6%2 == 0? → True  → expression: 6**2 = 36 → list mein add
Step 7: n = 7  → condition check: 7%2 == 0? → False → skip
Step 8: n = 8  → condition check: 8%2 == 0? → True  → expression: 8**2 = 64 → list mein add

Final result: [4, 16, 36, 64]
```

## Common Mistakes

1. **Readability ka issue**: Bahut complex comprehension likhna ("1 line mein sab kuch") code ko **padhna mushkil** bana deta hai. Rule of thumb: Agar expression 1 line mein fit nahi ho raha, toh normal loop use karo.

2. **Generator vs List confusion**:
   ```python
   # Yeh LIST comprehension hai (square brackets)
   [x for x in range(10)]  # list
    
   # Yeh GENERATOR hai (parentheses)
   (x for x in range(10))  # generator object
   ```

3. **Set comprehension vs Dict comprehension**:
   ```python
   # SET comprehension — single expression
   {x for x in range(5)}        # {0, 1, 2, 3, 4}
    
   # DICT comprehension — key:value pair
   {x: x**2 for x in range(5)} # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
   ```

4. **Variable shadowing**: Comprehension ke andar variable bahar ke variable ko overwrite kar sakta hai:
   ```python
   x = "outside"
   result = [x**2 for x in range(5)]  # x ab integer ban gaya!
   print(x)  # 4 (last value) — careful!
   ```

5. **Overusing nested comprehensions**: 2 se zyada nested loops comprehensions mein nahi dalne chahiye:
   ```python
   # Yeh padhna mushkil hai
   bad = [[[a*b*c for a in range(3)] for b in range(3)] for c in range(3)]
    
   # Better: normal loops
   good = []
   for a in range(3):
       for b in range(3):
           for c in range(3):
               good.append(a*b*c)
   ```

## Interview Notes

1. **List comprehension is faster than for loop**: Internally, list comprehension C level pe optimized hota hai, jabki for loop interpreter level pe chalta hai. Performance test:
   ```python
   import timeit
   # List comp: 0.5 seconds (approx)
   # For loop: 0.8 seconds (approx)
   ```

2. **Generator expressions save memory**: Jab large data pe kaam karo, generator expression use karo. List comprehension pura result memory mein store karta hai.

3. **Walrus operator with comprehension (Python 3.8+)**:
   ```python
   # := operator ko comprehension mein bhi use kar sakte ho
   data = [1, 2, 3, 4, 5]
   [y for x in data if (y := x*2) > 5]
   ```

4. **Nested comprehensions ka performance**: Badhiya hota hai kyunki internally optimized hota hai, lekin readability compromise hoti hai.

5. **List comprehension vs map()/filter()**: Comprehensions zyada readable aur Pythonic hain. Map/filter functional programming style hai.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** 1 se 10 tak ke numbers ke squares ki list comprehension se list banao.
2. **(Basic)** Ek list `[1, 2, 3, 4, 5, 6]` se list comprehension ka use karke sirf odd numbers filter karo.
3. **(Medium)** Ek dictionary `{
"a": 1, "b": 2, "c": 3}` ke keys aur values ko swap (invert) karne ke liye dictionary comprehension likho.
4. **(Medium)** Ek nested list (matrix) `[[1, 2], [3, 4]]` ko flatten karke `[1, 2, 3, 4]` banane ke liye list comprehension likho.
5. **(Hard)** Generator expression ka use karke `range(1, 1000000)` ke numbers ke squares generate karo aur print karo ki iska memory size normal list comprehension se kitna kam hai.
