import numpy as np

v1 = np.random.randint(1, 50, 10)

maxi = np.max(v1)
mini = np.min(v1)

count = np.sum((v1 > mini) & (v1 < maxi))

print("Vector:", v1)
print("Maximum value:", maxi)
print("Minimum value:", mini)
print("Elements between max and min:", count)
