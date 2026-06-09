import numpy as np

angles_deg = np.array([0, 30, 45, 60, 90])
angles_rad = np.deg2rad(angles_deg)

print("Angle  Sin   Cos   Tan")
for d, s, c, t in zip(angles_deg,
                     np.sin(angles_rad),
                     np.cos(angles_rad),
                     np.tan(angles_rad)):
    print(d, round(s,2), round(c,2), round(t,2))
