import pandas as pd

# Q3: Filtering data based on conditions
data = {'Student': ['Ravi', 'Sita', 'Gita', 'Mohan'], 'Marks': [45, 89, 72, 33]}
df = pd.DataFrame(data)

# Students who scored more than 50
passed_students = df[df['Marks'] > 50]

print("--- Students with > 50 marks ---")
print(passed_students)
