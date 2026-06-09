import numpy as np
import math

v1 = np.random.randint(1, 10, 2)
v2 = np.random.randint(1, 10, 2)

len_v1 = np.linalg.norm(v1)
len_v2 = np.linalg.norm(v2)

v1Norm = v1 / len_v1
v2Norm = v2 / len_v2

dot = np.dot(v1, v2)
angle_rad = math.acos(dot / (len_v1 * len_v2))
angle_deg = math.degrees(angle_rad)

print("v1:", v1)
print("v2:", v2)
print("Length of v1:", len_v1)
print("Length of v2:", len_v2)
print("Normalized v1:", v1Norm)
print("Normalized v2:", v2Norm)
print("Angle (radian):", angle_rad)
print("Angle (degree):", angle_deg)
