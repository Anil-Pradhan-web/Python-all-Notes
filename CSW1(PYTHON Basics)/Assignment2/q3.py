stack = []

def push(x): stack.append(x)
def pop(): return stack.pop() if stack else None
def display(): print(stack)
def is_empty(): return not stack

def eval_rpn(expr):
    for t in expr.split():
        if t.isdigit(): push(int(t))
        else:
            b, a = pop(), pop()
            push(eval(f"{a}{t}{b}"))
    return pop()

print("Result:", eval_rpn("5 3 4 * +"))
