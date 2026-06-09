# Classes and Objects

## Simple Explanation (Hinglish)
Socho ek car ki factory hai. Factory mein ek 'blueprint' (naksha) hota hai jisme likha hota hai ki car mein 4 pahiye honge, ek steering hoga, aur color red hoga. Is nakshan (blueprint) ko **Class** bolte hain. 
Ab us blueprint ko dekh kar factroy waalon ne 10 real cars bana di. In real cars ko **Objects** bolte hain. Class bas ek idea hai, Object ek sacchi cheez hai jo memory leti hai.

## Theory (Clear + Structured)
Object-Oriented Programming (OOP) is a paradigm based on the concept of "objects".
- **Class**: A blueprint for creating objects, providing initial values for state (member variables or attributes), and implementations of behavior (member functions or methods).
- **Object**: An instance of a class. When a class is defined, no memory is allocated until an object of that class is created.
- **`__init__()` (Constructor)**: A special method automatically called when an object is created. Used to initialize attributes.
- **`self`**: Represents the instance of the class itself. It binds the attributes with the given arguments.

## Syntax
```python
class ClassName:
    def __init__(self, parameters):
        self.attribute = parameters
    
    def method_name(self):
        # logic

object_name = ClassName(arguments)
```

## Examples

```python
# Example 1: Basic Class and Object
class Dog:
    # Constructor
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
    
    # Method
    def bark(self):
        print(f"{self.name} is barking! Woof!")

# Creating objects
dog1 = Dog("Tommy", "Pug")
dog2 = Dog("Max", "Husky")

print(dog1.name) # Output: Tommy
dog2.bark()      # Output: Max is barking! Woof!
```

## Dry Run / Explanation
* `class Dog`: Humne Dog naam ka naya blueprint banaya. (Humesha Class ka naam capital letter se start karte hain).
* `__init__`: Jaise hi main line 12 pe `dog1 = Dog("Tommy", "Pug")` likhunga, python immediately `__init__` ko run karega. `name` mein "Tommy" aayega aur wo `self.name` mein save ho jayega hamesha ke liye. 
* `self`: `self` bas ye batata hai ki value kis specific object ki hai (e.g. `dog1` ki ya `dog2` ki).

## Common Mistakes
1. Forgetting `self` in method definitions inside a class will throw a TypeError: `bark() takes 0 positional arguments but 1 was given`.
2. Initializing attributes outside of `__init__` making them class-level variables (shared amongst all objects) instead of instance-level variables.

## Interview Notes
1. **Class vs Instance Attributes**: Variables defined inside `__init__` using `self` are instance variables (unique for each object). Variables defined directly inside the class but outside any method are Class variables (shared by all).
2. `self` is not a keyword. You can name it anything (like `this`), but `self` is a universally accepted convention.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Create a `Student` class with attributes `name` and `age`. Create an object and print its name.
2. **(Basic)** Create class `Rectangle` with length and breadth, add method to calculate area.
3. **(Medium)** Create class `BankAccount` with balance, deposit(), withdraw() methods with validation.
4. **(Medium)** Make class `ShoppingCart` with items list, add_item(), remove_item(), total() methods.
5. **(Hard)** Implement class `LinkedList` with Node inner class, append() and display() methods.
