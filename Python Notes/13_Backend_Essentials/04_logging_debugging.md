# Logging (Professional Debugging)

### Simple Explanation (Hinglish)
`print()` statements se debugging karna amateur tarika hai. Production code mein hum **Logging** use karte hain. Logging se hum different levels set kar sakte hain (INFO, ERROR, WARNING), aur logs ko files mein save kar sakte hain baad mein check karne ke liye.

### Theory (Clear + Structured)
- **Logging Levels**:
  - `DEBUG`: Detailed information for diagnosing problems.
  - `INFO`: Confirmation that things are working as expected.
  - `WARNING`: An indication that something unexpected happened.
  - `ERROR`: Due to a more serious problem, some function has not been performed.
  - `CRITICAL`: A very serious error, indicating inability to continue.
- **Handlers**: Define where logs go (console, file, email, etc.).
- **Formatters**: Define how logs look (timestamp, level, message).

### Examples with Hinglish Comments

```python
import logging

# Basic configuration - sabse pehle setup karo
logging.basicConfig(
    level=logging.DEBUG,  # Sabhi levels ke logs dikhenge
    format='%(asctime)s - %(levelname)s - %(message)s',
    # Format: Time - Level - Message
    filename='app.log',  # Logs is file mein save honge
    filemode='a'  # Append mode (purane logs delete nahi honge)
)

# Different logging levels
logging.debug("Yeh debug message hai - detailed info ke liye")
logging.info("Application start ho gaya")
logging.warning("Kuch unusual ho raha hai par application chal raha hai")
logging.error("Error aa gaya! Koi function fail ho gaya")
logging.critical("Bahot serious error! Application band hone wala hai")

# Real-world example: Function mein logging
def divide_numbers(a, b):
    logging.info(f"Divide function called with a={a}, b={b}")
    
    if b == 0:
        logging.error("Division by zero attempted!")
        return None
    
    result = a / b
    logging.debug(f"Result calculated: {result}")
    return result

# Testing
divide_numbers(10, 2)  # Success case
divide_numbers(10, 0)  # Error case

# Advanced: Multiple loggers for different modules
logger_db = logging.getLogger('database')
logger_api = logging.getLogger('api')

logger_db.info("Database connection established")
logger_api.warning("API rate limit approaching")
```

### Sample `app.log` File Output:
```
2024-01-15 10:30:45,123 - INFO - Application start ho gaya
2024-01-15 10:30:46,456 - INFO - Divide function called with a=10, b=2
2024-01-15 10:30:46,457 - DEBUG - Result calculated: 5.0
2024-01-15 10:30:47,789 - INFO - Divide function called with a=10, b=0
2024-01-15 10:30:47,790 - ERROR - Division by zero attempted!
```

### Common Mistakes
1. **Production mein DEBUG level chhod dena**: Production mein hamesha `INFO` ya `WARNING` level rakho, warna log file bahot badi ho jayegi.
2. **Sensitive data log karna**: Passwords, API keys, ya personal information kabhi mat log karo!

### Interview Notes
1. **Why logging over print()?**: Logging can be disabled/filtered without changing code, logs can be saved to files, and different levels provide context.
2. **Log rotation**: In production, use `RotatingFileHandler` to prevent log files from growing infinitely.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Configure logging to write only ERROR and CRITICAL messages to a file.
2. **(Basic)** Set up basic logging to print messages with timestamp and severity level to the console.
3. **(Medium)** Create a logger for a web scraper that logs each URL being scraped and any errors encountered.
4. **(Medium)** Write a function that performs division and logs an INFO message on success, and an ERROR message on division by zero.
5. **(Hard)** Implement log rotation using `RotatingFileHandler` so that when a log file reaches 5MB, it creates a new file automatically.
