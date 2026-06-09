import numpy as np

def analyze_matrix():
    # Step 1: Generate 4×5 matrix with row-wise ranges
    mat = np.zeros((4, 5), dtype=int)
    for i in range(4):
        mat[i] = np.random.randint(i + 1, i + 10, 5)  # (i+1) to (i+9)

    # Step 2: Row-wise mean and std
    row_mean = np.mean(mat, axis=1)
    row_std = np.std(mat, axis=1)

    # Column-wise mean and std
    col_mean = np.mean(mat, axis=0)
    col_std = np.std(mat, axis=0)

    # Step 3: Compare overall mean and std
    mean_result = "row-wise" if row_mean.mean() > col_mean.mean() else "column-wise"
    std_result = "row-wise" if row_std.mean() > col_std.mean() else "column-wise"

    # Step 4: Return result as dictionary
    return {
        "mean": mean_result,
        "std": std_result
    }

# Function call
result = analyze_matrix()
print(result)
