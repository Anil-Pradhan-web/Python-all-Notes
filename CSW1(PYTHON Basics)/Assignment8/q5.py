import numpy as np

# Blood sugar levels (mg/dL)
sugar = np.array([85, 110, 145, 95, 130, 160, 102, 98])

# Create empty array for classification
status = np.empty(sugar.shape, dtype=object)

# Boolean masks
normal = sugar < 100
prediabetic = (sugar >= 100) & (sugar <= 139)
diabetic = sugar >= 140

# Assign labels using masking
status[normal] = "Normal"
status[prediabetic] = "Pre-Diabetic"
status[diabetic] = "Diabetic"

print("Blood Sugar:", sugar)
print("Status:", status)
