# Person class
class Person:
    def __init__(self, gender):
        self.gender = gender


# College class (uses composition)
class College:
    def __init__(self):
        # Creating Person objects inside College
        self.student1 = Person("female")
        self.student2 = Person("male")


# Create College object
college = College()

# Print genders of both students
print("Student 1 Gender:", college.student1.gender)
print("Student 2 Gender:", college.student2.gender)
