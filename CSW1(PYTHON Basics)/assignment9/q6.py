import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 2*np.pi, 0.1)

plt.plot(x, np.sin(x), 'b-', label="Sine")
plt.plot(x, np.cos(x), 'r--', label="Cosine")
plt.xlabel("X values (radians)")
plt.ylabel("Function values")
plt.title("Sine and Cosine Functions")
plt.legend()
plt.show()
