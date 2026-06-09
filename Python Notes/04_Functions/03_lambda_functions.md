# Lambda, Map, Filter

## Simple Explanation (Hinglish)
Normal functions dher saari jagah aur lines lete hain. Agar koi aisa function banayana ho jo chota sa ho aur uska sirf ek bar use ho, to hum **lambda** use karte hain. Yeh 'anonymous' function hota hai jiska koi naam nahi hota.

## Theory (Clear + Structured)
- **Lambda Functions**: Small, anonymous functions created using the `lambda` keyword. They can take any number of arguments, but can only have **one expression**.
- **`map(function, iterable)`**: Applies the function to every item in the iterable (like list).
- **`filter(function, iterable)`**: Filters out elements from an iterable where the function returns False.

## Syntax
```python
lambda arguments : expression
```

## Examples

```python
# Example 1: Lambda basic
add = lambda x, y: x + y
print(add(5, 3)) # Output: 8

# Example 2: Map function
numbers = [1, 2, 3, 4]
squared = list(map(lambda x: x**2, numbers))
print(squared) # Output: [1, 4, 9, 16]

# Example 3: Filter function
ages = [12, 18, 24, 16, 30]
adults = list(filter(lambda x: x >= 18, ages))
print(adults) # Output: [18, 24, 30]
```

## Dry Run / Explanation
* `lambda x, y: x + y`: Humne function bina naam ka banaya jo 2 input `x` and `y` lega aur unka sum return karega. Uski definition ko hi variable `add` mein store kar diya.
* `map()`: Ye line by line kaam karta hai. numbers array uthaya, sabhi numbers ko individually lambda function mein feed kiya, answer nikala, aur new map object return kiya (`list()` usko array format mei laata hai).
* `filter()`: `ages` nikalega as `x`. Agar `x >= 18` True ho gaya, toh select kar lega, False ko hata dega.

## Common Mistakes
1. Trying to add multiple lines of logic in Lambda: Lambda strictly restricts you to a single expression. No loop or complex `if...else` statements can be nested directly.
2. Forgetting to cast `map` or `filter` objects to `list`. Doing `print(map(...))` will print a memory reference instead of values.

## Interview Notes
1. Why use Lambda? Lambda is extremely useful as arguments to higher-order functions like `sort()`, `map()`, and `filter()`. E.g., `data.sort(key=lambda x: x['age'])`.
2. **List Comprehension**: Map/Filter can usually be replaced by List Comprehensions which are more "Pythonic" (`[x**2 for x in numbers]`).

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a lambda function that multiples an argument `n` by 10.
2. **(Basic)** Use lambda with filter() to get numbers > 10 from list.
3. **(Medium)** Sort list of strings by their length using sorted() with lambda key.
4. **(Medium)** Use reduce() with lambda to find product of all list elements.
5. **(Hard)** Sort a list of tuples `[(1, 'B'), (3, 'A'), (2, 'C')]` primarily based on the second item in each tuple (string character) using `sorted()` and `lambda`.
