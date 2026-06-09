class Student:
    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no
        self.__marks = 0   # private variable

    # Setter method (with validation)
    def set_marks(self, marks):
        if 0 <= marks <= 100:
            self.__marks = marks
        else:
            print("Invalid marks! Marks must be between 0 and 100.")

    # Getter method
    def get_marks(self):
        return self.__marks

    # Grade calculation
    def calculate_grade(self):
        if self.__marks >= 90:
            return "A"
        elif self.__marks >= 80:
            return "B"
        elif self.__marks >= 70:
            return "C"
        elif self.__marks >= 60:
            return "D"
        elif self.__marks >= 50:
            return "E"
        else:
            return "F"

    # Display student details
    def show_details(self):
        print("Name       :", self.name)
        print("Roll No    :", self.roll_no)
        print("Marks      :", self.get_marks())
        print("Grade      :", self.calculate_grade())
        print("----------------------------")


# Main program

# Creating student objects
s1 = Student("Anil", 101)
s2 = Student("Rahul", 102)
s3 = Student("Priya", 103)

# Setting marks using setter method
s1.set_marks(92)
s2.set_marks(78)
s3.set_marks(45)

# Displaying student details
s1.show_details()
s2.show_details()
s3.show_details()
