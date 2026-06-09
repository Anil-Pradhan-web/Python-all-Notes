import numpy as np

# 14 days temperature data
temp = np.array([28, 32, 35, 36, 30, 29, 34, 37, 33, 31, 38, 27, 35, 34])

# Heat-wave days (≥ 35°C)
heat_wave = temp >= 35
print("Heat-wave days:", temp[heat_wave])

# Count heat-wave days
print("Number of heat-wave days:", np.sum(heat_wave))

# Replace temperatures below 30°C with 30
temp[temp < 30] = 30
print("After replacing <30°C with 30:", temp)

# Comfortable days (30°C to 34°C)
comfortable = (temp >= 30) & (temp <= 34)
print("Comfortable days:", temp[comfortable])

# Increase heat-wave temperatures by 2°C
temp[temp >= 35] += 2
print("After heat-wave correction:", temp)
