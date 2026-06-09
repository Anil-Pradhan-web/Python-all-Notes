import matplotlib.pyplot as plt

# Q7: Plotting a Bar Chart
categories = ['Python', 'Java', 'C++', 'JavaScript']
students = [40, 25, 15, 30]

plt.bar(categories, students, color=['blue', 'orange', 'green', 'red'])
plt.title("Favorite Programming Languages")
plt.xlabel("Languages")
plt.ylabel("Number of Students")
# plt.show() # Uncomment to view
print("Bar Chart logic executed.")
