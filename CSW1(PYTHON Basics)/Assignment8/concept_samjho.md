# Assignment 8: Data Computation with Numpy 🧮

Bhai, normal List data structure mathematical computation main boht dheemi (slow) hai aur vector multiplication allow nhi karti default pe. `numpy` library arrays optimized memory use karte that's why speed kafi tez result laita. Let's understand:

1. **Generating Fast Random vectors arrays (`np.random.randint`) :**
   - Tumhe 10 item list chaye randomly ? Tum 10 time `for loop` daal kar generate ke array insert karna parega list pe par. Numpy arrays direct one line call `np.random.randint(low, high, size)` call ke exact fast output assign kardeti hi us particular variable pe vector/grid format mien. 

2. **Aggregations Builtin Method (`np.max(v1)`, `np.min()`):**
   - Matlab yaha hum loop pe check nahi karrahe array index by index loop likar... Vectorized data k upper functions like `np.max()`, array ka top sabse bada item C level par turant scan out karke laa deta hai list mai se bina loop logic load kiye tumhare system per.
   
3. **Array Filtering And Masking Process:**
   - Numpy mai elements select filter logic array pe tagda kam krta ,`count = np.sum((v1 > mini) & (v1 < maxi))`. Condition elements array se single filter mask nikaal layega  aur true count batadega without iterating the array index manually!
