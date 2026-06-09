class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def __str__(self):
        return f"{self.name}({self.species})"


# Creating an object of Animal class
animal1 = Animal("Lucy", "Cat")

# Printing the object
print(animal1)
