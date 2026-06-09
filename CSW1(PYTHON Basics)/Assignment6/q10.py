class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll
        self.__marks = 0

    def set_marks(self, m):
        if 0 <= m <= 100:
            self.__marks = m

    def get_marks(self):
        return self.__marks

    def grade(self):
        return ("A" if self.__marks >= 90 else
                "B" if self.__marks >= 80 else
                "C" if self.__marks >= 70 else
                "D" if self.__marks >= 60 else
                "E" if self.__marks >= 50 else "F")

    def show(self):
        print(self.name, self.roll, self.get_marks(), self.grade())


# Objects
s1 = Student("Anil", 101)
s2 = Student("Rahul", 102)
s3 = Student("Priya", 103)

# Set marks
s1.set_marks(92)
s2.set_marks(78)
s3.set_marks(45)

# Display details
s1.show()
s2.show()
s3.show()
