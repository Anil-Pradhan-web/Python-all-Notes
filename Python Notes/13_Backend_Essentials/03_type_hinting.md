# Type Hinting (Modern Python)

### Simple Explanation (Hinglish)
Python dynamically typed hai (variable ka type batane ki zaroorat nahi), lekin bade projects mein yeh confusion create karta hai ki function mein kaunsa data ja raha hai. **Type Hinting** se hum explicitly bata sakte hain ki variable ka type kya hai. Yeh code run nahi rokta, bas readability badhata hai aur IDEs ko help karta hai.

### Theory (Clear + Structured)
- **Type Hints**: Annotations that specify the expected data types of variables, function parameters, and return values.
- Introduced in Python 3.5+ via PEP 484.
- Tools like `mypy` can check type errors before running code.

### Examples with Hinglish Comments

```python
from typing import List, Dict, Optional, Union

# Simple type hint for variables
name: str = "Rahul"
age: int = 25
price: float = 99.99
is_active: bool = True
# # Variables ke saath unka type likh diya - yeh sirf documentation hai

# Function with type hints
def greet_user(username: str, age: int) -> str:
    # username string hai, age integer hai, aur function string return karega
    return f"Hello {username}, you are {age} years old"

# List type hint
fruits: List[str] = ["apple", "banana", "cherry"]
numbers: List[int] = [1, 2, 3, 4, 5]
# # List mein kis type ke elements hain woh specify kiya

# Dictionary type hint
user_data: Dict[str, Union[str, int]] = {
    "name": "Aman",
    "age": 30,
    "city": "Delhi"
}
# # Dict mein keys string hain, values ya to string ya int ho sakti hain

# Optional type hint (None bhi ho sakta hai)
def find_user(user_id: int) -> Optional[str]:
    # Ya to user name return hoga (string), ya None agar user na mile
    if user_id == 1:
        return "Rahul"
    return None

# Complex example with nested types
def process_orders(orders: List[Dict[str, Union[str, float]]]) -> float:
    # Orders ek list hai, jisme dictionaries hain
    # Har dict mein string keys hain aur values ya string ya float
    total = 0.0
    for order in orders:
        total += order.get("amount", 0.0)
    return total

# Testing
print(greet_user("Priya", 28))  # Hello Priya, you are 28 years old
print(find_user(1))  # Rahul
print(find_user(99))  # None
```

### Common Mistakes
1. **Type hints ko strict validation samajhna**: Type hints runtime pe error nahi fenkte. Wo sirf documentation ke liye hain.
2. **Har jagah type hint lagana**: Chhote scripts mein zaroori nahi, lekin bade projects mein best practice hai.

### Interview Notes
1. **Does Python enforce types?**: No, Python doesn't enforce type hints at runtime. They're for static analysis tools like `mypy`.
2. **Benefits**: Better IDE autocomplete, easier code maintenance, self-documenting code.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Add type hints to a function that takes two integers and returns their sum.
2. **(Basic)** Define a variable with a type hint for a string and an integer, and assign values to them.
3. **(Medium)** Create a function that accepts a list of strings and returns a dictionary with word counts. Add proper type hints.
4. **(Medium)** Write a function that takes a dictionary containing keys as strings and values as union of strings/integers, and prints all values.
5. **(Hard)** Write a custom generic-like function that handles database connection responses, using type annotations like `Optional` and `Union`.
