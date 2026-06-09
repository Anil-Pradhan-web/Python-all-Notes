# Data Science Libraries (NumPy & Pandas)

## Simple Explanation (Hinglish)
- **NumPy**: Normal Python ki list me numbers daal ke math karna bohot slow hota hai. NumPy ek super-fast library hai jo calculations array banakar milliseconds me kar deti hai.
- **Pandas**: Agar aapke paas ek badi Excel file ya CSV hai jisme thousands of rows hain, aur aapko unko filter karna hai, toh Pandas ka use hota hai. Yeh tables (DataFrames) banane ke kaam aata hai.

## Theory (Clear + Structured)
- **NumPy (Numerical Python)**: Used for working with arrays. It provides a high-performance multidimensional array object (`ndarray`) and tools for working with these arrays.
- **Pandas**: Built on top of NumPy, it provides data structures like `Series` (1D) and `DataFrame` (2D table) designed for quick data analysis, filtering, and cleaning.

## Syntax
```python
import numpy as np
import pandas as pd

# Creating numpy array
arr = np.array([1, 2, 3])

# Creating pandas dataframe
df = pd.DataFrame(data_dict)
```

## Examples

```python
import numpy as np
import pandas as pd

# --- NumPy Example ---
print("--- NumPy ---")
arr = np.array([1, 2, 3, 4, 5])
print(arr * 2) # Multiplies 2 to ALL elements at once: [2, 4, 6, 8, 10]

# Generate random numbers
random_grid = np.random.rand(2, 2)
print(random_grid)

# --- Pandas Example ---
print("\n--- Pandas ---")
data = {
    "Name": ["Rahul", "Alia", "Neha"],
    "Age": [25, 22, 24],
    "City": ["Delhi", "Mumbai", "Pune"]
}

df = pd.DataFrame(data)
print("Original Table:")
print(df)

# Filtering data
print("\nPeople older than 23:")
print(df[df["Age"] > 23])
```

## Dry Run / Explanation
* `arr * 2`: Vectorization kehte hain isse. Normal python list pe `* 2` karne se list 2 baar jud jati hai (e.g., `[1,2,1,2]`). Lekin NumPy list ke andar ghus kar uske har element ko 2 se multiply karta hai. C/C++ backend ki wajah se ye extremely fast hai.
* `pd.DataFrame(data)`: Hamari normal dictionary ko utha kar usne rows columns wali ek badhiya beautiful table (Data Frame) me tabdeel kar diya, jiske column headings keys se uthaye gaye.
* `df[df["Age"] > 23]`: Pandas DataFrame ke andar humne ek aisi condition pass ki jo sirf wo column aur row validate karke deti hai jahan Age column me value 23 se badi ho.

## Common Mistakes
1. Trying to append items continuously inside a NumPy array. NumPy arrays have fixed sizes! If you append, it actually creates a brand-new array in memory which is slow.
2. Forgetting to install the libraries via `pip install numpy pandas`. They don't come directly bundled with raw Python.

## Interview Notes
1. **Why is NumPy faster than Python Lists?** NumPy arrays are stored at one continuous place in memory unlike lists, so processes can access and manipulate them very efficiently. Also, the core logic is written in C.
2. What does `df.head()` do? It quickly shows the first 5 rows of a huge dataset. Interviewers love hearing dataframe manipulation techniques.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** NumPy array banao, shape aur mean print karo.
2. **(Basic)** Pandas DataFrame banao from dict: {"name":["A","B"],"age":[25,30]}.
3. **(Medium)** CSV load karo, describe() print karo.
4. **(Medium)** DataFrame filter karo where age > 25.
5. **(Hard)** Group by category, mean calculate karo, result JSON mein save karo.