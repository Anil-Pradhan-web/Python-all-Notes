import struct

num = 1025

little = struct.pack("<H", num)
big = struct.pack(">H", num)

print("Little Endian:", little)
print("Big Endian:", big)
