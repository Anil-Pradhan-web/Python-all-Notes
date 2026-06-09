# Arrays, Stacks, and Queues

## Simple Explanation (Hinglish)
- **Arrays (Lists in Python)**: Samajh lo books ek shelf me randomly rakhi hui hain.
- **Stacks (LIFO)**: Ek ke upar ek plates ka bundle. Sabse upar jo plate last me rakhi thi, wahi sabse pehle utha paoge (Last In First Out).
- **Queues (FIFO)**: Movie ticket ki line. Jo sabse pehle khada hoga, usko sabse pehle ticket milega (First In First Out).

## Theory (Clear + Structured)
- **Arrays**: Native `list` in Python acts as a dynamic array. Elements are stored consecutively.
- **Stack**: Follows **LIFO** principle. Operations: `push` (append at end), `pop` (remove from end).
- **Queue**: Follows **FIFO** principle. Operations: `enqueue` (add to end), `dequeue` (remove from front). Using normal Python lists for Queues is slow `O(n)` because elements must shift. `collections.deque` is the proper way.

## Syntax
```python
# Stack
stack = []
stack.append(item) # Push
stack.pop()        # Pop

# Queue using deque
from collections import deque
queue = deque()
queue.append(item)    # Enqueue
queue.popleft()       # Dequeue
```

## Examples

```python
# Example 1: Stack Implementation
print("--- STACK ---")
stack = []

# Push elements
stack.append("A")
stack.append("B")
stack.append("C")
print("Stack size:", len(stack))

# Pop elements (LIFO)
top = stack.pop()
print("Removed:", top) # C
print("Stack now:", stack)

# Example 2: Queue using collections.deque
from collections import deque

print("\n--- QUEUE ---")
queue = deque(["Person 1", "Person 2"])

# Enqueue
queue.append("Person 3")

# Dequeue (FIFO)
first = queue.popleft()
print("Served:", first) # Person 1
print("Queue now:", list(queue))
```

## Dry Run / Explanation
* `stack.append("C")`: Stack ke end me store hoga. Jab `.pop()` kiya, default Python `pop()` hamesha list ka aakhiri element delete karta hai, isliye "C" bahar aaya. List me append aur pop memory efficient hain (O(1) time).
* `deque()` ka popleft: Jab movie wali line me aage se "Person 1" ko ticket mila, to normal array se agar usko delete karte toh baaki sab logo ko shift hona padta apne places se (O(n) time). Par deque "Double Ended Queue" ka abbreviation hai jo bina shifting kiye pehle element ko constant time (O(1)) me delete ya nikal deta hai!

## Common Mistakes
1. Using `.pop(0)` on a standard Python list to implement a Queue. It works, but it forces every other element to shift memory locations, severely destroying performance for large lists. Always use `collections.deque`.
2. Popping from an empty stack/queue without checking if it has elements will throw an `IndexError`.

## Interview Notes
1. Reversing a string or balancing parentheses is the most famous Stack interview question. 
2. BFS (Breadth-First Search) traverses graphs/trees level-by-level, which requires Queues. DFS (Depth-First Search) requires Stacks.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Implement a Stack using a class with `push`, `pop`, `peek`, and `is_empty` methods.
2. **(Basic)** Implement a Queue using `collections.deque` and demonstrate enqueue/dequeue operations.
3. **(Medium)** Valid Parentheses Problem: Use a stack to check if a string like `"( { [ ] } )"` has correctly closed brackets. (Very common interview question!)
4. **(Medium)** Write a function to reverse a string using a Stack.
5. **(Hard)** Implement a custom Queue using Two Stacks. (Tricky, requires moving elements back and forth between stack1 and stack2).
