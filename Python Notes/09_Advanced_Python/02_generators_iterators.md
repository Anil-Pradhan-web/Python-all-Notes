# Generators and Iterators

## Simple Explanation (Hinglish)
Maan lo aapko 1 crore random numbers chahiye. Agar aap wo saare numbers ek list me daalke return karwayoge, to program fat jayega kyunki itna RAM hi nahi hoga memory mein (List sab kuch ek sath memory me latati hai).
**Generator** ek smart tarika hai, ye "ek baar mein ek" number lauta-ta hai. Usko pichla record bhulne ki aadat hoti hai. Ye data list ki tarah generate toh karega, par memory space zero lega! Ye jaadu `yield` keyword se hota hai.

## Theory (Clear + Structured)
- **Iterator**: An object that contains a countable number of values. It implements two predefined methods: `__iter__()` and `__next__()`. Lists, Sets, Dictionaries are Iterables but not iterators until `iter()` is called on them.
- **Generator**: A special type of function that returns an *iterator* object. Instead of using `return`, generators use the `yield` keyword. 
- When an execution hits `yield`, the function's state is paused and saved. The next time it runs, it resumes right from where it left off!

## Syntax
```python
def my_generator():
    yield value1
    yield value2
```

## Examples

```python
# Example 1: Basic Generator
def count_to_three():
    print("Start")
    yield 1
    print("Middle")
    yield 2
    print("End")
    yield 3

# Generators don't execute immediately! They return a generator object.
gen = count_to_three()

# We use next() to get the next yielded value
print(next(gen)) # Start \n 1
print(next(gen)) # Middle \n 2 

# Example 2: Real-world memory efficient Generator
def infinite_squares():
    n = 1
    while True:
        yield n * n
        n += 1

squares_gen = infinite_squares()
print(next(squares_gen)) # 1
print(next(squares_gen)) # 4
print(next(squares_gen)) # 9
```

## Dry Run / Explanation
* `yield 1`: Jab `next(gen)` call hota hai pehli baar, function line 1 se start hota hai "Start" print karta hai aur `1` pe pause ho jata hai (return ki tarah lauta deta hai). Par memory mein save rakhta hai.
* Jab dobara `next(gen)` call hua, toh wo line 1 se nahi start hota. Wo `yield 1` ke theek baad wali line ("Middle") pe aake resume hota hai!
* `infinite_squares` ek aisi machine ban gayi jo kabhi nahi rukegi, lekin yeh code crash kabhi error nahi dega RAM bharne ka kyunki numbers tabhi generate honge jab demand hogi (Lazy Evaluation).

## Common Mistakes
1. Calling a function with `yield` directly expecting return values. `func()` returns a generator object, which means you MUST loop over it or use `next(func())` to get its values.
2. Assuming `next()` will loop infinitely. Once the generator hits the end, calling `next()` again raises a `StopIteration` error. (For loops handle this error automatically).

## Interview Notes
1. **Generator vs Return**: `return` ends a function completely and destroys local variables. `yield` pauses the function and preserves local variables to resume later.
2. Generator Expressions: You can create generators on the fly using brackets `(x * x for x in range(10))`. Very similar to list comprehension but uses parenthesis. Faster and highly memory efficient!

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write a generator function that yields the days of the week one by one.
2. **(Basic)** Create a generator that yields numbers from 1 to 5 one by one.
3. **(Medium)** Create a generator that yields even numbers up to `100` and stop.
4. **(Medium)** Write a generator that yields squares of numbers from 1 to N.
5. **(Hard)** Implement your own `range()` function using a generator that takes `start`, `stop`, and `step` to yield numbers.
