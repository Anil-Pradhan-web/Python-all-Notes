# Environment Variables & Security

### Simple Explanation (Hinglish)
Code mein passwords, API keys, ya database URLs hard-code karna bahot dangerous hai! Agar code GitHub pe daala to sab kuch leak ho jayega. **Environment Variables** se hum sensitive data ko alag `.env` file mein rakhte hain jo Git pe upload nahi hoti.

### Theory (Clear + Structured)
- **Environment Variables**: Dynamic values that can affect the way running processes behave on a computer.
- **`.env` file**: A text file containing key-value pairs for configuration.
- **`python-dotenv`**: Library to load `.env` files in Python.
- **Best Practice**: Never commit `.env` files to version control.

### Examples with Hinglish Comments

```python
# Pehle install karo: pip install python-dotenv

from dotenv import load_dotenv
import os

# .env file se variables load karna
load_dotenv()

# Ab environment variables access kar sakte ho
DATABASE_URL = os.getenv("DATABASE_URL")
# # DATABASE_URL variable .env file se utha liya

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False")
# # Second argument default value hai agar variable na mile

print(f"Database: {DATABASE_URL}")
print(f"API Key: {API_KEY}")
print(f"Debug Mode: {DEBUG_MODE}")

# Safe credential handling example
def connect_to_database():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables!")
    
    # Connection code here...
    print(f"Connecting to {db_url}...")
    return "Connected!"

# Testing
try:
    connect_to_database()
except ValueError as e:
    print(f"Error: {e}")
```

### Sample `.env` File:
```bash
# .env file (ISE GIT PE MAT DALNA!)
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=sk-1234567890abcdef
SECRET_KEY=my-super-secret-key-123
DEBUG_MODE=True
EMAIL_PASSWORD=email_password_here
```

### Sample `.gitignore` File:
```bash
# .gitignore mein yeh add karo
.env
venv/
__pycache__/
*.log
```

### Common Mistakes
1. **`.env` file ko Git pe push karna**: Hamesha `.gitignore` mein `.env` add karo.
2. **Default values na dena**: `os.getenv("KEY", "default")` use karo taaki error na aaye.
3. **Production mein .env rely karna**: Production mein environment variables directly server pe set karo.

### Interview Notes
1. **Why not hardcode secrets?**: Hardcoded secrets can be exposed through version control, decompilation, or accidental sharing.
2. **12-Factor App**: Methodology that recommends storing config in environment variables.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Create a `.env` file with a variable `APP_NAME` and print it in Python.
2. **(Basic)** Retrieve an environment variable with a default fallback value if the key does not exist.
3. **(Medium)** Build a script that reads API credentials from `.env` and makes a request to an API (or prints the config details securely).
4. **(Medium)** Write a class `Config` that loads configurations like DB_PORT, DB_HOST from `.env` and validates they are not empty.
5. **(Hard)** Create a configuration class that loads all settings from environment variables with proper validation and typecasting (e.g. converting `DEBUG_MODE=True` string to a real boolean).
