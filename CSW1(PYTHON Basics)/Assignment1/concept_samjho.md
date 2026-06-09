# Assignment 1: Functions, Strings aur Dictionaries 🚀

Bhai, is assignment mein tumne basic Python logic ko implement kiya hai. Dhyan se samjho:

1. **Functions & Default Arguments (`def generate_bill(...)`):**
   - Python mein function banate waqt hum default values set kar sakte hain (jaise `discount=0`). Agar call karte time koi value nahi deta, toh ye default value use ho jati hai.
   - Named arguments (`discount=5`) ka use karke tum specifically kisi specific argument ko value pass kar sakte ho, position ki tension bina.

2. **String Manipulation:**
   - Strings *immutable* hoti hain. Yahan `.replace()`, `.lower()`, aur `.split()` ka use karke tumne kisi bhi string ki safai ki hai (punctuation remove karke word-by-word break karna).
   
3. **Dictionaries (Word Frequency Count karna):**
   - `word_count.get(word, 0) + 1` boht tagda aur repeated use hone wala logic hai. Yeh check karta hai ki agar word dictionary mein hai toh purani value dega, warna 0 dega. Fir `+1` karke nayi count update kar dega.
   - Items ko sort karna: `sorted(dict.items())` dictionary ko list of tuples mein convert karke alphabetically sort kar deta hai.
