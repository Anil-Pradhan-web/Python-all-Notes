# Lists and Tuples

## Simple Explanation (Hinglish)
List aur Tuple dono collection of items hote hain. Jaise aap bazaar jane se pehle ek shopping list banate ho jisme items hote hain, Python mein bhi list waisi hi hoti hai. 
List aur Tuple mein main farq kya hai? List ke items ko aap baad mein change kar sakte ho (modify/add/remove), par Tuple ek baar ban gaya toh fix ho jata hai, usko change nahi kar sakte.

## Theory (Clear + Structured)
- **List**: An ordered, mutable (changeable) collection of items. Enclosed in square brackets `[]`.
- **Tuple**: An ordered, immutable (unchangeable) collection of items. Enclosed in parentheses `()`.

Both lists and tuples can hold heterogenous data types (a mix of int, strings, floats, etc.).

## Syntax
```python
# List syntax
my_list = [item1, item2, item3]

# Tuple syntax
my_tuple = (item1, item2, item3)
```

## Examples

```python
# Example 1: Lists Methods
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")    # Adds to the end
fruits.insert(1, "mango")  # Inserts at index 1
fruits.pop()               # Removes the last item
fruits[0] = "kiwi"         # Modifying an item
print(fruits) # Output: ['kiwi', 'mango', 'banana', 'cherry']

# Example 2: Tuples
coordinates = (10.0, 20.0)
# coordinates[0] = 15.0  --> This will throw a TypeError!
print(coordinates[1]) # Output: 20.0

# Example 3: Unpacking a Tuple
a, b = coordinates
print("X:", a, "Y:", b)
```

## Dry Run / Explanation
* `fruits.insert(1, "mango")`: List mein index 0 se shuru hota hai. Toh ye "mango" ko 1st index par daal dega, aur "banana", "cherry" sab aage shift ho jayenge.
* `tuple error`: Tuple banne ke baad update nahi hota. Agar aap `coordinates[0] = 15` karoge, Python gussa ho jayega kyunki Tuple 'immutable' hai.

## Common Mistakes
1. **Index Boundary**: Trying to access an element that does not exist (`IndexError: list index out of range`).
2. **Single Element Tuple**: Writing `tup = (5)` creates an integer, not a tuple. For a one-element tuple, you MUST add a comma: `tup = (5,)`.

## Interview Notes
1. **List vs Tuple memory**: Tuples take slightly less memory and are faster than lists because of immutability.
2. Tuples can be used as keys in a dictionary because they are immutable; lists cannot.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** List banao [10,20,30,40,50]. First, last element aur length print karo.
2. **(Basic)** Tuple (5,10,15) mein 20 add karne ki koshish karo (error dekho).
3. **(Medium)** User se 5 numbers lo, list mein store karo, sum aur average nikaalo.
4. **(Medium)** Do lists concatenate karo, sort karo, reverse karo.
5. **(Hard)** Duplicates hatao using set: [1,2,2,3,4,4,5]