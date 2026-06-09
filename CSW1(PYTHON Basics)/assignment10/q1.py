import pandas as pd

# Q1: Create a DataFrame from a dictionary and print it
data = {
    'Name': ['Amit', 'Raj', 'Simran', 'Pooja', 'Rahul'],
    'Age': [20, 21, 19, 22, 20],
    'Marks': [85, 78, 92, 88, 76]
}
df = pd.DataFrame(data)

print("--- DataFrame from Dictionary ---")
print(df)
