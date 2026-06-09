import matplotlib.pyplot as plt

# Q8: Plotting a Scatter Plot
height = [150, 160, 165, 170, 175, 180]
weight = [50, 55, 60, 68, 70, 80]

plt.scatter(height, weight, color='purple', marker='x')
plt.title("Height vs Weight")
plt.xlabel("Height (cm)")
plt.ylabel("Weight (kg)")
# plt.show() # Uncomment to view
print("Scatter Plot logic executed.")
