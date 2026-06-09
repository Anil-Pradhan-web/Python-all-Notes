class Demo:
    def __new__(cls):
        print("__new__ method called (object creation)")
        obj = object.__new__(cls)   # manually create object
        return obj

    def __init__(self):
        print("__init__ method called (object initialization)")


# Create object
d = Demo()


class MyInt(int):
    def __new__(cls, value):
        print("__new__ called for immutable int")
        value = value * 10     # modify value at creation time
        return super().__new__(cls, value)

    def __init__(self, value):
        print("__init__ called (value already fixed)")


# Create object
x = MyInt(5)
print("Final value:", x)
