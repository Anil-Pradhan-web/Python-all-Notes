import random

students = ["John", "Riya", "Meera", "Amit",
            "Rahul", "Zara", "Sneha", "Kunal"]

random.shuffle(students)

print("Team A:", students[0], ",", students[1])
print("Team B:", students[2], ",", students[3])
print("Team C:", students[4], ",", students[5])
print("Team D:", students[6], ",", students[7])
