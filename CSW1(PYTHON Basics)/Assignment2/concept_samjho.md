# Assignment 2: Python Data Structures 🏗️ (List, Tuple, Set, Dict)

Bhai, Python mein Data Structures boht important hain. Iss assignment ka real focus collection of data ko handle karna tha:

1. **Lists aur Unki Flexibility:**
   - List *mutable* hoti hai, isme data change kar sakte hain. `sum()`, `max()`, `min()` direct list pe operate hote hain.
   - `scores.sort(reverse=True)` wali line se descending order mein sort ho jata hai.
   - **Slicing:** `scores[-3:] = [0, 0, 0]` - list ke last 3 elements pakdna aur unko 0 se replace karne ka direct tarika.

2. **List Comprehensions (Ek line ka jaadu):**
   - `[s for s in scores if s > avg]` -> Multiple line ka `for` aur `if` loop ek hi line mein likhne ko list comprehension kehte hain. Industry mein yahi use hota hai code ko clean jaldi aur fast run karne ke liye.

3. **Dictionaries & Dictionary Comprehensions:**
   - `{s["info"][1]: sum(...) for s in students}` -> Jaise list ko ek line me generate karte hain, waise hi Dict ko yahan generate kiya hai name aur uske total/avg marks se map karne ke liye.
   - Sets ka use: Skills wale data ko sets (`{"Python", "C"}`) mein rakha hai. Sets fast hote hain aur unme duplicate values nahi aati.
