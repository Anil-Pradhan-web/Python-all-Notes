import numpy as np

def normalize_3d():
    # Generate 3D array (example: 3×4×5)
    arr = np.random.rand(3, 4, 5)

    # Normalize along each dimension
    arr_norm = (arr - arr.min(axis=0)) / (arr.max(axis=0) - arr.min(axis=0))

    return arr_norm

result = normalize_3d()
print(result)
