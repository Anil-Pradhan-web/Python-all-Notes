def generate_bill(item, price, quantity=1, discount=0, taxrate=0.05):
    # Step 1: Calculate subtotal
    subtotal = price * quantity
    
    # Step 2: Apply discount
    discount_amount = subtotal * (discount / 100)
    discounted_total = subtotal - discount_amount
    
    # Step 3: Apply tax
    tax_amount = discounted_total * taxrate
    final_total = discounted_total + tax_amount
    
    # Step 4: Print detailed bill summary
    print("------ BILL SUMMARY ------")
    print(f"Item Name   : {item}")
    print(f"Quantity    : {quantity}")
    print(f"Price       : ₹{price}")
    print(f"Discount    : {discount}%")
    print(f"Tax Rate    : {taxrate * 100}%")
    print(f"Subtotal    : ₹{subtotal:.2f}")
    print(f"Discount Amt: ₹{discount_amount:.2f}")
    print(f"Tax Amount  : ₹{tax_amount:.2f}")
    print(f"Total Bill  : ₹{final_total:.2f}")
    print("--------------------------\n")

# (i) Using only required arguments
generate_bill("Book", 500)

# (ii) Providing a custom quantity (default discount and tax)
generate_bill("Pen", 20, 10)

# (iii) Using named arguments for discount and tax (default quantity)
generate_bill("Shoes", 2000, discount=10, taxrate=0.08)

# (iv) Providing all arguments explicitly
generate_bill("Laptop", 50000, 2, 10, 0.05)
