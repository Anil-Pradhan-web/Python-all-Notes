import numpy as np
import matplotlib.pyplot as plt

v1 = np.array([3, 4])
v2 = np.array([1, 2])

# Normalize vectors
v1 = v1 / np.linalg.norm(v1)
v2 = v2 / np.linalg.norm(v2)

# Plot vectors
plt.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='green', label='v1')
plt.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color='red', label='v2')

plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.axhline(0)
plt.axvline(0)
plt.legend()
plt.title("Normalized Vectors from Origin")
plt.show()
