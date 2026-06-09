# Encapsulation and Abstraction

## Simple Explanation (Hinglish)
- **Encapsulation**: Maan lo ek capsule dwaai hai jiske andar chemical band hai, taaki bahar se koi virus usko effect na kar paye. Coding mein apne variable ko 'private' banane ko Encapsulation kehte hain, ki koi bahar se sidha aake data badal na sake.
- **Abstraction**: Car chalate waqt aap steering gumate ho car ghum jati hai. Engine ke andar piston kaise upar-neeche ho raha hai usse aapko matblab nahi. Yeh hai Abstraction! Jo complex cheezen hain unhe chhupa do.

## Theory (Clear + Structured)
- **Encapsulation**: The bundling of data (attributes) and methods that act on the data into a single unit (class). It also involves hiding internal state by making attributes private (using `_` or `__` prefixes) and providing public getter and setter methods to access them securely.
- **Abstraction**: Hiding the complex implementation details and showing only the essential features of the object. Achieved in Python using the `abc` (Abstract Base Classes) module.

## Examples

```python
# Example 1: Encapsulation (Private variables)
class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance  # Double underscore makes it Private!

    # Getter method
    def get_balance(self):
        return self.__balance

    # Setter method
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

acc = BankAccount("Rahul", 1000)
# print(acc.__balance)  # This will throw an AttributeError!
print(acc.get_balance()) # Output: 1000

# Example 2: Abstraction
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass # Must be implemented by child classes

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        return 3.14 * self.radius * self.radius

# shape = Shape()  # Error! Cannot instantiate an abstract class
circle = Circle(5)
print(circle.area()) # 78.5
```

## Dry Run / Explanation
* `self.__balance`: Double underscore lagane se Python Name Mangling use karke element ko direct access block kar direct edit block kar deta hai. Isko `acc.deposit(50)` karke hi modify kar sakte hain, direct nahi. Isse security aati hai.
* `Shape(ABC)`: Humne Shape ko Abstract bana diya. Humne rule bana diya ki `area()` sabko apna banana padega. Agar kal koi `Rectangle` child class banti hai, usko compulsory `area()` likhna padega otherwise error aayega.

## Common Mistakes
1. Using single underscore `_variable` and expecting errors. In Python, single underscore is just a convention meaning "please don't touch this", but it doesn't actually stop you. True private is double underscore `__variable`.
2. Forgetting to write the `@abstractmethod` decorator above your abstract methods in the base class.

## Interview Notes
1. Python doesn't have strict 'public', 'protected', and 'private' keywords like Java/C++. It relies on naming conventions (`_` protected, `__` private via name mangling).
2. **What is Name Mangling?** If you name `__balance` inside `BankAccount`, python renames it internally to `_BankAccount__balance`.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Try to access the `__balance` variable of the BankAccount class directly using Name Mangling trick mentioned in Interview Notes.
2. **(Basic)** Create class with private `__password`, add setter with validation (min 8 chars).
3. **(Medium)** Create a `Student` class with private `__marks`. Write a setter function that ensures someone cannot set marks > 100.
4. **(Medium)** Create abstract class `Database` with abstract connect(), query(), close() methods.
5. **(Hard)** Create an abstract class `Vehicle` with an abstract method `fuel_efficiency()`. Implement child classes `Bike` and `Truck` returning their specific efficiencies.
