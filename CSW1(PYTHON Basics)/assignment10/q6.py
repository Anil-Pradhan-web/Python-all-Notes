import matplotlib.pyplot as plt

# Q6: Plotting a basic Line Graph
x = [1, 2, 3, 4, 5]
y = [10, 25, 40, 50, 70]

plt.plot(x, y, color='blue', marker='o', linestyle='--')
plt.title("Simple Line Plot")
plt.xlabel("X-Axis (Days)")
plt.ylabel("Y-Axis (Growth)")
# plt.show() # Uncomment to see the graph locally
print("Line Plot logic executed.")
