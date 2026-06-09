# Define the Car class
class Car:
    def __init__(self, v1, v2):
        self.make = v1
        self.model = v2

    # Getter methods
    def get_make(self):
        return self.make

    def get_model(self):
        return self.model

    # Setter methods
    def set_make(self, v1):
        self.make = v1

    def set_model(self, v2):
        self.model = v2



car1 = Car("Toyota", "Corolla")

car2 = Car(None, None)

print("Car 1 Details:")
print("Make:", car1.get_make())
print("Model:", car1.get_model())

print("\nCar 2 Details:")
print("Make:", car2.get_make())
print("Model:", car2.get_model())


car2.set_make("Honda")
car2.set_model("Civic")

print("\nUpdated Car 2 Details:")
print("Make:", car2.get_make())
print("Model:", car2.get_model())
