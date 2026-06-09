# Linked Lists and Trees

## Simple Explanation (Hinglish)
- **Linked List**: Normal list ek dabbe ki tarah hai jisme fixed khaane hote hain. Linked list chitiyon ki line jaisa hai. Har element (Node) ke paas apni value hoti hai, aur uske paas uske aage wale node ka "Pata" (Memory Address) hota hai. 
- **Tree**: Family tree jaisa! Sabse upar Dada (Root node), fir uske bache, fir unke bache. Binary Tree matlab zyada se zyada bas 2 hi bache ho sakte hain (Left and Right).

## Theory (Clear + Structured)
- **Linked List**: A linear data structure composed of Nodes. Each node stores `data` and a reference (`next`) to the next node. Allows for fast insertions/deletions without shifting elements!
- **Tree**: A hierarchical structure consisting of nodes. 
    - **Root**: Topmost node.
    - **Leaf Node**: A node with no children.
    - **Binary Tree**: A tree whose nodes have at most two children.
    - **BST (Binary Search Tree)**: Left child is smaller than parent, right child is greater. Extremely fast for searching!

## Examples

```python
# Example 1: Singly Linked List Node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Pointer to next node

# Connecting nodes manually
head = Node(10)
second = Node(20)
third = Node(30)

head.next = second    # 10 -> 20
second.next = third   # 20 -> 30

# Traversal / Printing
current = head
while current is not None:
    print(current.data, end=" -> ")
    current = current.next
print("None")


# Example 2: Simple Binary Tree Node
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Making a tiny tree:
#       1
#      / \
#     2   3
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
```

## Dry Run / Explanation
* Linked list execution starting head tak aati hai: `current = head`. Fir while loop check karta hai ki wahan koi value hai? Hai. Usne 10 print kiya. Fir `current.next` ne current ki location ko agle node `second` par skip kar diya. Ye cycle tabhi toot ti hai jab hume aage koi address nahi milta (`None`).
* Tree ke andar, hum array indexes ka use nahi karte. Hum left aur right child assign kar dete hain taaki data inherently hierarchically store ho jaaye. 

## Common Mistakes
1. Completely losing track of the `head` pointer in a Linked List. If you move `head = head.next` while iterating, you lose access to the actual start of your Linked List permanently! Always create a temporary variable `current = head`.
2. Causing an infinite loop by creating physical cycles in Linked Lists (A points to B, B points to A).

## Interview Notes
1. **Reversing a Linked List**: Be absolutely prepared for this. It involves carefully updating pointers (`prev`, `current`, `next_node`) continuously without breaking the chain.
2. In-order Traversal of a BST directly gives a sorted array natively. They will ask you how traversing left, root, right works via recursion.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Add a method `insert_at_beginning(data)` to a Linked List class to dynamically prepend new nodes.
2. **(Basic)** Create a Binary Tree node class and make a tree with a root and two child nodes.
3. **(Medium)** Find the middle element of a Linked List in one pass (Hint: Use tortise and hare / Slow and Fast pointers).
4. **(Medium)** Implement In-order traversal of a Binary Tree recursively.
5. **(Hard)** Write a recursive function to calculate the maximum depth (height) of a given Binary Tree.
