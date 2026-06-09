import pandas as pd
import matplotlib.pyplot as plt

# Q10: Connecting Pandas directly with Matplotlib
data = {
    'Year': [2018, 2019, 2020, 2021, 2022],
    'Revenue': [1000, 1500, 1200, 2000, 2500]
}
df = pd.DataFrame(data)

# Using pandas inbuilt plot wrapper over matplotlib
df.plot(kind='line', x='Year', y='Revenue', color='red', marker='o')
plt.title("Revenue Over Years")
plt.ylabel("Revenue in USD")
# plt.show() # Uncomment to view
print("Pandas + Matplotlib Intengration logic executed.")
