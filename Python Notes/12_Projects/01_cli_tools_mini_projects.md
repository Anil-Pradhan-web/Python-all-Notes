# Projects and CLI Tools

## Simple Explanation (Hinglish)
Apne jitna bhi python abhi tak padha (variables, files, requests, OOP), jab tak un sab components ko jodd kar ek useable application nahi banta, knowledge raw hi rehti hai. Terminal/Command Line Interface (CLI) apps banana project journey ke liye sabse best kickstart hai. GUI (Graphical) banaye bina backend logic strong ho jata hai.

## Theory (Clear + Structured)
Building Mini Projects allows you to:
1. Master structure & modules natively.
2. Practice File handling to store configs/databases.
3. Fetch data dynamically via APIs.
4. Improve your logic building.

### Recommended Tooling for CLI:
- **`argparse`** module: Python's standard library to read arguments from the terminal (e.g., `python script.py --name Rahul`).
- **`sys.argv`**: A more primitive way to read bash arguments.

## Example: Building a Tiny CLI To-Do App

```python
import sys
import os

FILE_NAME = "tasks.txt"

def display_tasks():
    if not os.path.exists(FILE_NAME):
        print("No tasks found! Enjoy your day.")
        return
    with open(FILE_NAME, "r") as file:
        tasks = file.readlines()
        if not tasks:
            print("To-Do list is completely empty!")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task.strip()}")

def add_task(task_name):
    with open(FILE_NAME, "a") as file:
        file.write(task_name + "\n")
    print(f"Added task: '{task_name}'")

# Simple Router based on sys.argv
if __name__ == "__main__":
    # Ensure there is an argument passed
    if len(sys.argv) < 2:
        print("Usage: python todo.py [view | add]")
        sys.exit()

    command = sys.argv[1]

    if command == "view":
        display_tasks()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task! Ex: python todo.py add 'Read book'")
        else:
            tasktext = " ".join(sys.argv[2:])
            add_task(tasktext)
    else:
        print("Unknown command.")
```

## Dry Run / Explanation
* `sys.argv`: Ye ek list hai jismein aap jo terminal mein command likhte ho, wo automatically array index ke format mein aa jata hai. 
* Agar aapne likha `python todo.py view`. To `sys.argv[0]` = "todo.py" aur `sys.argv[1]` = "view". 
* Agar command "add" aayi, toh hum bache hue saare words join karke `tasks.txt` mein write/append kardenge. Agli baar `view` command daalne par, waha se items fetch hoke terminal me dikh jayenge!

## Project Ideas For Resume 
*(Go build these immediately)*

1. **Weather CLI App**: Use the `requests` library to fetch weather utilizing an OpenWeatherMap API key (Search: `python weather.py --city Mumbai`).
2. **Password Generator & Manager**: Encrypts and stores strong random passwords using file handling and OOP structures. 
3. **Web Scraper (Amazon/Flipkart Tracker)**: Use `BeautifulSoup` to scrape item price every hour. If the price drops below limit, send an Email via `smtplib` module!
4. **Expense Tracker**: Saves daily spending into a `.csv` file via simple command inputs, and generates total metrics utilizing Pandas DataFrame groups!

## Career Advice (Interview Notes)
1. Hosting code on GitHub with proper ReadMe instructions (`How to run my app`) is crucial. Companies look at projects before your degree.
2. Separate your code! Put database logic in `storage.py`, models in `models.py`, API fetches in `network.py`, and run everything via `main.py`. This Modularization tells interviewers you write Production-ready code!

---
> **You have successfully finished the entire Python Core to Advanced Curriculum!** Keep practicing these patterns, build those logic blocks, and happy coding! 🚀
