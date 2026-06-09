# Assignment 4: Regular Expressions (Regex) 🔍

Bhai, yeh assignment data validations jaisi cheezon ke liye sabse important Regular Expression (Regex) concept par based tha.

1. **`re` module in Python:**
   - Jab hume complex patterns dna/data filter aur validity check karni ho (Jaise Email original formated hai na, ya phone number exactly 10 digits ka hai?), toh hum in-built library `import re` (Regular Expression) module use karte hain.
   
2. **Regex Patterns ka kamaal (`r'...'`)**
   - Ek ajeeb sa code, pattern kehlata hai: `r'^[A-Za-z0-9]...@[A-Za-z]+\.[A-Za-z]{2,4}$'` yeh ek "Raw String" pattern hai .
   - `^` batata hai string exactly yaha se start honi chahiye.
   - `[A-Za-z0-9]` set batata hai ki agla character alphabet ya number me se hi ek hona chahiye.
   - `@` direct email symbol check ke liye dala gaya hai.
   - `\.[A-Za-z]{2,4}`: check karta hai ek "." (dot) aur baad mei kam se kam 2 aur maximum 4 characters (.com, .net, .in).
   - `$` sign pattern ka end secure kar deta hai ki pichhe kuch arbitrary letters na ho ab.
   
3. **`re.match()` ya `re.search()` se verify:**
   - `re.match(pattern, text)` compare karta hai ki wo particular text (email) hamare banaye hue strict rules (pattern) pe completely fit baith rahi hai ya nahi.
