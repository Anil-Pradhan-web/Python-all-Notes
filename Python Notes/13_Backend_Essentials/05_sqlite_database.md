# Database Integration with SQLite

### Simple Explanation (Hinglish)
Backend developer ka main kaam hota hai data ko store karna aur retrieve karna. **SQLite** ek lightweight database hai jo Python ke saath built-in aati hai. Isme server ki zaroorat nahi hoti, seedha file mein data store hota hai. Seekhne ke liye perfect hai!

### Theory (Clear + Structured)
- **SQLite**: Serverless, self-contained SQL database engine.
- **CRUD Operations**: Create, Read, Update, Delete - basic database operations.
- **Cursor**: Object used to execute SQL queries.
- **Connection**: Object representing the database connection.

### Examples with Hinglish Comments

```python
import sqlite3

# Step 1: Database connection banana (file automatically ban jayegi)
conn = sqlite3.connect('my_database.db')
# # Agar file nahi thi to nayi ban jayegi, warna existing open ho jayegi

cursor = conn.cursor()
# # Cursor se hum queries execute karenge

# Step 2: Table banana
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
# # Users table bana diya with columns: id, name, email, age, created_at

conn.commit()
# # Changes ko permanently save karna zaroori hai

# Step 3: Data insert karna (CREATE)
def add_user(name, email, age):
    try:
        cursor.execute('''
            INSERT INTO users (name, email, age) 
            VALUES (?, ?, ?)
        ''', (name, email, age))
        # # ? placeholders hain SQL injection se bachne ke liye
        conn.commit()
        print(f"User {name} added successfully!")
    except sqlite3.IntegrityError:
        print(f"Email {email} already exists!")

add_user("Rahul", "rahul@example.com", 25)
add_user("Priya", "priya@example.com", 28)
add_user("Aman", "aman@example.com", 30)

# Step 4: Data read karna (READ)
cursor.execute('SELECT * FROM users')
all_users = cursor.fetchall()
# # Saare users fetch kar liye list mein

print("\nAll Users:")
for user in all_users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Age: {user[3]}")

# Specific user dhundhna
cursor.execute('SELECT * FROM users WHERE age > ?', (26,))
older_users = cursor.fetchall()
print("\nUsers older than 26:")
for user in older_users:
    print(f"{user[1]} is {user[3]} years old")

# Step 5: Data update karna (UPDATE)
cursor.execute('''
    UPDATE users 
    SET age = ? 
    WHERE email = ?
''', (29, "priya@example.com"))
conn.commit()
print("\nPriya's age updated to 29")

# Step 6: Data delete karna (DELETE)
cursor.execute('DELETE FROM users WHERE name = ?', ("Aman",))
conn.commit()
print("Aman deleted from database")

# Step 7: Connection close karna
conn.close()
```

### SQL Injection Prevention
```python
# GALAT TARIKA (SQL Injection vulnerable):
# cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# SAHI TARIKA (Parameterized query):
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
# # Humesha ? placeholder use karo user input ke saath
```

### Common Mistakes
1. **`commit()` bhool jana**: Insert/Update/Delete ke baad `commit()` nahi kiya to changes save nahi honge!
2. **Connection close nahi karna**: Hamesha `conn.close()` karo ya `with` statement use karo.
3. **SQL Injection**: User input ko directly query mein mat daalo, hamesha parameterized queries use karo.

### Interview Notes
1. **What is ACID?**: Atomicity, Consistency, Isolation, Durability - properties that guarantee reliable database transactions.
2. **SQLite vs MySQL/PostgreSQL**: SQLite is file-based (good for small apps/testing), while MySQL/PostgreSQL are server-based (good for production).

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Create a database with a `products` table having columns: id, name, price, quantity.
2. **(Basic)** Insert a single row into the `products` table and select it.
3. **(Medium)** Write functions to add, view, update, and delete products from the database.
4. **(Medium)** Query the `products` table to find all items with price greater than 500.
5. **(Hard)** Create two tables `customers` and `orders` with a foreign key relationship. Write a query to get all orders for a specific customer.
