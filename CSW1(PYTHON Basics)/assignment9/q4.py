import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 50)

plt.plot(x, np.sin(x), label="Sin")
plt.plot(x, np.cos(x), label="Cos")
plt.plot(x, np.tan(x), label="Tan")
plt.legend()
plt.show()
