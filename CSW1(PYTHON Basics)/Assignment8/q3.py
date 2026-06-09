import numpy as np
import random
import time

# -------- NumPy Method --------
start = time.time()
arr_np = np.random.random((1000, 1000))
end = time.time()
numpy_time = end - start

# -------- Python Nested Loop Method --------
start = time.time()
arr_py = []
for i in range(1000):
    row = []
    for j in range(1000):
        row.append(random.random())
    arr_py.append(row)
end = time.time()
python_time = end - start

print("NumPy execution time:", numpy_time)
print("Python execution time:", python_time)

if numpy_time < python_time:
    print("NumPy method is faster")
else:
    print("Python nested loop method is faster")
