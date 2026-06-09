import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-20, 25, 100)
y1 = x**3 - 15*x**2 + 25
y2 = 2*x**2 - 10*x + 5

plt.plot(x, y1, color='blue', label="y1")
plt.plot(x, y2, color='red', linestyle='--', label="y2")
plt.title("Polynomial Functions")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()
