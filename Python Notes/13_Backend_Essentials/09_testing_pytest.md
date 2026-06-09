# Testing with pytest

### Simple Explanation (Hinglish)
Code likhna kaafi nahi, yeh ensure karna bhi zaroori hai ki code sahi kaam kar raha hai. **Testing** se hum automatically check kar sakte hain ki hamara code break to nahi ho raha. **pytest** Python ka most popular testing framework hai.

### Theory (Clear + Structured)
- **Unit Testing**: Testing individual functions/components in isolation.
- **Test Cases**: Specific scenarios to test (normal input, edge cases, errors).
- **Assertions**: Statements that check if a condition is true.
- **Fixtures**: Reusable setup code for tests.

### Examples with Hinglish Comments

```python
# Pehle install karo: pip install pytest

# File: calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

def is_even(n):
    return n % 2 == 0

# File: test_calculator.py (TEST FILE)
import pytest
from calculator import add, divide, is_even

# Test functions must start with 'test_'
def test_add_positive_numbers():
    assert add(2, 3) == 5
    # # Check karo ki 2+3=5 hai

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_mixed_numbers():
    assert add(-1, 1) == 0

def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    # # Check karo ki error raise ho raha hai
    with pytest.raises(ValueError):
        divide(10, 0)

def test_is_even():
    assert is_even(4) == True
    assert is_even(7) == False

# Parametrized tests (ek test multiple inputs ke liye)
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add_multiple_cases(a, b, expected):
    assert add(a, b) == expected
    # # Yeh test 4 baar chalega different inputs ke saath

# Fixtures - reusable setup
@pytest.fixture
def sample_data():
    return {"name": "Rahul", "age": 25}

def test_fixture_usage(sample_data):
    assert sample_data["name"] == "Rahul"
    assert sample_data["age"] == 25
```

### Running Tests
```bash
# Terminal mein run karo:
pytest
# # Saare tests run ho jayenge

pytest -v
# # Verbose mode - detailed output

pytest test_calculator.py::test_add_positive_numbers
# # Sirf ek specific test run karo

pytest --cov=calculator
# # Code coverage dekho (kitna code test ho raha hai)
```

### Common Mistakes
1. **Tests na likhna**: Production code mein kam se kam 70-80% code covered hona chahiye tests se.
2. **Complex tests**: Tests simple aur readable hone chahiye.
3. **Testing implementation instead of behavior**: Test karo ki function kya karta hai, na ki kaise karta hai.

### Interview Notes
1. **TDD (Test Driven Development)**: Pehle test likho, fir code likho jo test pass kare.
2. **CI/CD**: Tests automatically run hote hain jab code push karte ho (GitHub Actions, Jenkins).

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Write tests for a function that checks if a number is prime.
2. **(Basic)** Run a basic test suite using `pytest -v` command and view the report.
3. **(Medium)** Create tests for a function that validates email addresses.
4. **(Medium)** Write a pytest fixture that provides sample mock database connections or configuration dictionaries.
5. **(Hard)** Write parametrized tests for a sorting function with multiple edge cases (empty list, duplicates, large lists).
