# Assignment 3: Basic Input/Output aur Logic 💻

Is assignment mein syntax, basic operations, and logic sikhaya gaya hai. Yahan jyada heavy algorithms nahi balki foundation set ki gayi hai:

1. **Smart Multiple Line Inputs:**
   - `x, y, z = map(int, input().split())` -> Yeh competitive programming aur assignments mein bahut use hota hai. Ek single line space-separated string ko `split()` karta hai, aur sab parts pe `int` mapping kar deta hai. Return list unpack hoke x, y, z ko mil jati hai. 

2. **Pythonिक Variable Swapping:**
   - Doosri languages mein temp variable lena padta hai: `temp=x; x=y; y=temp;`.
   - Lekin yahan direct: `y, z = z, y`.
   - Yeh exactly kaam kaise karta hai? Right side mein ek temporary `(z, y)` ka tuple banta hai aur Left side ke variables mein directly unpack ho kar assign ho jata hai. Fast and reliable!

3. **f-Strings (Formatted Strings):**
   - Pehle string print karne me boht `+` and `,` lagane padte the. Ab `print(f"x={x}, y={y}")` use hota hai. Strings ke aandar simple braces `{}` lagao and apna variable ya equation dalo. Values replace ho jayengi.
