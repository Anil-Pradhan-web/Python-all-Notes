while True:
    user_input = input("Enter (add/sub/mul/div) or 'exit': ").strip()
    
    if user_input.lower() == "exit":
        print("Exiting the program.")
        break

    parts = user_input.split()
    if len(parts) != 3:
        print("Invalid input.")
        continue

    op, a, b = parts[0], float(parts[1]), float(parts[2])

    if op == "add":
        print("Result:", a + b)
    elif op == "sub":
        print("Result:", a - b)
    elif op == "mul":
        print("Result:", a * b)
    elif op == "div":
        if b == 0:
            print("Error: Division by zero")
        else:
            print("Result:", a / b)
    else:
        print("Invalid operation.")

