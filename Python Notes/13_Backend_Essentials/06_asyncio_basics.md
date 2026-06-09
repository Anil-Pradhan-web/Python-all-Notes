# AsyncIO Basics (Asynchronous Programming)

### Simple Explanation (Hinglish)
Normal Python code line-by-line chalta hai (synchronous). Agar ek line mein 5 second ka wait hai, to poora code ruk jata hai. **AsyncIO** se hum multiple tasks ko "concurrently" chala sakte hain. Jaise ek waiter ek table se order leta hai, kitchen ko deta hai, aur dusre table pe chala jata hai - wait nahi karta!

### Theory (Clear + Structured)
- **async/await**: Keywords for defining and using coroutines.
- **Coroutine**: A function that can pause its execution and resume later.
- **Event Loop**: Manages and executes asynchronous tasks.
- **Use Cases**: Web scraping, API calls, file I/O, database queries.

### Examples with Hinglish Comments

```python
import asyncio
import time

# Normal synchronous function (slow)
def fetch_data_sync(task_name, delay):
    print(f"Started {task_name}")
    time.sleep(delay)  # Poora program ruk jata hai
    print(f"Finished {task_name}")
    return f"Data from {task_name}"

# Asynchronous function (fast)
async def fetch_data_async(task_name, delay):
    print(f"Started {task_name}")
    await asyncio.sleep(delay)  # Sirf yeh task rukega, baaki chalte rahenge
    print(f"Finished {task_name}")
    return f"Data from {task_name}"

# Synchronous execution (total time: 1+2+3 = 6 seconds)
start = time.time()
fetch_data_sync("Task 1", 1)
fetch_data_sync("Task 2", 2)
fetch_data_sync("Task 3", 3)
print(f"Synchronous total time: {time.time() - start:.2f} seconds\n")

# Asynchronous execution (total time: ~3 seconds - sab parallel chale!)
async def main():
    # Saare tasks ek saath start honge
    results = await asyncio.gather(
        fetch_data_async("Task 1", 1),
        fetch_data_async("Task 2", 2),
        fetch_data_async("Task 3", 3)
    )
    # gather() sab tasks complete hone ka wait karega
    print(f"\nResults: {results}")

start = time.time()
asyncio.run(main())
print(f"Asynchronous total time: {time.time() - start:.2f} seconds")

# Real-world example: Multiple API calls
async def fetch_user_data(user_id):
    print(f"Fetching data for user {user_id}...")
    await asyncio.sleep(1)  # Simulating API call
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_all_users():
    user_ids = [1, 2, 3, 4, 5]
    # Saare API calls parallel mein honge
    tasks = [fetch_user_data(uid) for uid in user_ids]
    users = await asyncio.gather(*tasks)
    return users

# Running the async function
all_users = asyncio.run(fetch_all_users())
print(f"\nFetched {len(all_users)} users concurrently!")
```

### Common Mistakes
1. **`await` bhool jana**: Async function ko call karte waqt `await` lagana zaroori hai.
2. **Blocking calls in async code**: `time.sleep()` mat use karo, `await asyncio.sleep()` use karo.
3. **Overusing async**: CPU-intensive tasks ke liye async faydemand nahi hai, sirf I/O bound tasks ke liye use karo.

### Interview Notes
1. **When to use AsyncIO?**: Use for I/O-bound tasks (network requests, file operations, database queries). Not for CPU-bound tasks.
2. **GIL (Global Interpreter Lock)**: Python's GIL prevents true parallelism in threads, but async works around this for I/O operations.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Create an async function that prints numbers from 1 to 5 with 1-second delay.
2. **(Basic)** Write an async function that prints "Hello" and awaits another async function that prints "World".
3. **(Medium)** Write an async program that fetches data from 3 different "fake APIs" (use asyncio.sleep) concurrently.
4. **(Medium)** Run a list of async tasks concurrently using `asyncio.gather` and capture their return values.
5. **(Hard)** Create an async web scraper structure (simulated with random sleep) that scrapes multiple URLs simultaneously without blocking.
