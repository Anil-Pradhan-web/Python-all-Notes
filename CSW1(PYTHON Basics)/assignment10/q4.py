import pandas as pd
import numpy as np

# Q4: Handling Missing Values (NaN)
data = {'Item': ['Apple', 'Banana', 'Orange', 'Mango'], 'Price': [50, np.nan, 30, np.nan]}
df = pd.DataFrame(data)

print("--- Original Data ---")
print(df)

# Fill missing values with a default value (e.g. 40)
filled_df = df.fillna(40)
print("\n--- Filled Missing Values Data ---")
print(filled_df)
