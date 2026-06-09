import struct

nums = [10, 20, 30, 40, 50]

with open("numbers.bin", "wb") as f:
    for n in nums:
        f.write(struct.pack("i", n))

print("Integers written to binary file successfully.")

result = []
with open("numbers.bin", "rb") as f:
    while True:
        data = f.read(4)
        if not data:
            break
        result.append(struct.unpack("i", data)[0])

print("Integers read from file:", result)
