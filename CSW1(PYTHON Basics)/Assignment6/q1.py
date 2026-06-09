# Define the Student class
class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

    def display(self):
        print(f"Name: {self.name}, Roll Number: {self.roll}")

students = []

n = int(input("Enter number of students: "))


for i in range(n):
    print(f"\nEnter details of student {i+1}")
    name = input("Enter name: ")
    roll = input("Enter roll number: ")

   
    student = Student(name, roll)
    students.append(student)

print("\n--- Student Details ---")
for student in students:
    student.display()
