class Product:
    # Class variable
    total_products_sold = 0

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    # Instance method
    def sell_product(self, amount):
        if amount <= self.quantity:
            self.quantity -= amount
            Product.total_products_sold += amount
            print(f"{amount} units of {self.name} sold.")
        else:
            print("Not enough quantity available.")

    # Class method
    @classmethod
    def get_total_products_sold(cls):
        return cls.total_products_sold


# Main program

# Create product objects
p1 = Product("Laptop", 60000, 10)
p2 = Product("Mobile", 20000, 15)

# Sell products
p1.sell_product(3)
p2.sell_product(5)

# Display remaining quantities
print("\nRemaining Stock:")
print("Laptop Quantity:", p1.quantity)
print("Mobile Quantity:", p2.quantity)

# Display total products sold
print("\nTotal Products Sold:", Product.get_total_products_sold())
