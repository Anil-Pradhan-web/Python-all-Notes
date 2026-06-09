# Assignment 6: Object-Oriented Programming (OOPs) 🏗️

Bhai, this assignment Object-Oriented Programming samajhne wala ek game-changer pattern hai jise professional engineers use kartein hain. Iss concept main real-world ko "classes (blueprint)" and "Objects (Item)" mein implement kara jata h!

1. **Classes aur Objects (Factory and Product):**
   - `class Student:` tumhari ek nayi factory ka layout (blueprint) hai jo batata hai ki is category mein ek student kiske form mein dikhta hai(kya kya properties/Data attributes aur methods holds karega).
   - Jab us category ka instance bulaya gaya , like `s1 = Student("Ram", 21)`. toh ab us physical object jo Ram hai usko hi "Object" kahan jayega.

2. **The Constructor Logic - `__init__(self, ...)`:**
   - Dhyan do in Built-in dunder-methods par! Jaise hi ek object setup karte hou (`s1 = Student(..)`), toh background se automatically `__init__` constructor function invoke hota hi or initial values allocate karta hi data-elements par pehle se.
   - Yeh `self` keyword actually Object "apna pointer" deta hi jiski madad se wo data modify and attach kar sakhta hi apne saath (`self.name = 'Ram'`). Yeh sabse zruri hai taaki Python confuse na ho dusre Student se!

3. **Objects ke Apne Methods (Behaviors):**
   - Class scope ke ander methods yani "apne functions", unme parameters dete waqt `(self)` hamesha as a first argument lagana compulsory hai syntax hisaab se. `def display(self):` is object particular values (`self.name`) fetch kardeta output me.
