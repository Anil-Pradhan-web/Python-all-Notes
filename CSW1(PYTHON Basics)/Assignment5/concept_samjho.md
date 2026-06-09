# Assignment 5: File System aur Handing (I/O) 📂

Isse pehle console par aane wala temporary result close karne par gayab ho jata tha. Yeh assignment local permanent Files ke andar kaise save/read karein sikhati hai.

1. **`with open(...) as f:` - The Modern Protocol:**
   - File ko old way mai aise open karte the: `f = open('file.txt', 'r')` aur kaam ke baad manually `f.close()` lagana padta tha takke background me memory leak na ruke. 
   - Par Context Manager yaani `with open(...)` use karne se scope ke aandar file read/write ho jati hai aur uske block ke bahar aate hi automatically file close ho jati hai background mei bina humari tension ke.

2. **Reading and Writing Modes ka system (`r`, `w`, `a`):**
   - **Mode `"w"` (Write):** Humara data `f.write("A")` file me write hoga, par purana sab delete kareke naye suruu se overwrite kar dega, aur file na bani hogi to nayi file save kar dega system pe.
   - **Mode `"r"` (Read):** File me mojud data ko nikal ke `f.read()` dwara le aana program ki window (terminal) me dikhane ya manipulate karne ke liye kaam aata hai.
   
3. **Iterating over loops and line breaks:**
   - Ek simple loop use karke saare list ki students item ko `f.write(name + "\n")` ki tarah "\n" (new line enter function) deke direct permanently Hard Disk mei feed kar diya gaya. 
