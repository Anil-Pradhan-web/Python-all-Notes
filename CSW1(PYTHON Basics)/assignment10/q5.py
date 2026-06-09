import pandas as pd

# Q5: Grouping data (GroupBy operations)
data = {
    'Department': ['IT', 'HR', 'IT', 'Marketing', 'HR'],
    'Salary': [60000, 45000, 70000, 50000, 40000]
}
df = pd.DataFrame(data)

# Group by department and find average salary
avg_salary_df = df.groupby('Department')['Salary'].mean()

print("--- Average Salary per Department ---")
print(avg_salary_df)
