import pandas as pd

# Q2: Basic Data Inspection using Pandas
data = {'Name': ['A', 'B', 'C', 'D', 'E'], 'Score': [10, 20, 30, 40, 50], 'Passed': [False, False, True, True, True]}
df = pd.DataFrame(data)

print("--- First 2 rows ---")
print(df.head(2))

print("\n--- Data Summary ---")
print(df.describe())
