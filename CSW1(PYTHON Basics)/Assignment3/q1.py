x, y, z = map(int, input("Enter three numbers: ").split())
print(f"Before swapping: x={x}, y={y}, z={z}")
y, z = z, y
print(f"After swapping:  x={x}, y={y}, z={z}")
