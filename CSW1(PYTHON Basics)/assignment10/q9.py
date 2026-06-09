import matplotlib.pyplot as plt
import numpy as np

# Q9: Generating a Histogram
# Simulating the age of 100 people using random module
data = np.random.randint(18, 60, 100)

plt.hist(data, bins=10, color='teal', edgecolor='black')
plt.title("Age Distribution Histogram")
plt.xlabel("Age Group")
plt.ylabel("Frequency")
# plt.show() # Uncomment to view
print("Histogram logic executed.")
