# Data Analysis Projects — Pandas ke Saath Real Projects

## Simple Explanation (Hinglish)
Ab tak jo kuch seekha (lists, dicts, pandas, file handling) — ab woh real data pe apply karo. Data analysis ka matlab hai **raw data se meaningful insights nikaalna**.

## Project 1: Student Marks Analyzer 🎓
```python
import pandas as pd
import json

# Sample data
data = {
    "students": [
        {"name": "Alice", "math": 85, "science": 90, "english": 78},
        {"name": "Bob", "math": 92, "science": 88, "english": 95},
        {"name": "Charlie", "math": 70, "science": 75, "english": 72},
    ]
}

# CSV mein save karo
df = pd.DataFrame(data["students"])
df.to_csv("students.csv", index=False)

# Analysis
df = pd.read_csv("students.csv")
print("Average marks per subject:")
print(df[["math", "science", "english"]].mean())

df["total"] = df["math"] + df["science"] + df["english"]
df["percentage"] = df["total"] / 3

# Top student
top_student = df.loc[df["percentage"].idxmax()]
print(f"\n🥇 Top Student: {top_student['name']} - {top_student['percentage']:.1f}%")

# Save results
df.to_json("results.json", orient="records", indent=2)
```

## Project 2: Sales Data Analysis 📊
```python
import pandas as pd
import json
from datetime import datetime

# Create sample sales data
sales_data = [
    {"date": "2024-01-01", "product": "Laptop", "price": 50000, "qty": 2},
    {"date": "2024-01-02", "product": "Mouse", "price": 500, "qty": 10},
    {"date": "2024-01-03", "product": "Laptop", "price": 50000, "qty": 1},
    {"date": "2024-01-04", "product": "Keyboard", "price": 1500, "qty": 5},
]

df = pd.DataFrame(sales_data)
df["total_sale"] = df["price"] * df["qty"]
df["date"] = pd.to_datetime(df["date"])

# Analysis
print("💰 Total Revenue:", df["total_sale"].sum())
print("📦 Most Sold Product:", df.groupby("product")["qty"].sum().idxmax())
print("📈 Average Order Value: ₹", round(df["total_sale"].mean(), 2))

# Best selling products
product_summary = df.groupby("product").agg(
    total_qty=("qty", "sum"),
    total_revenue=("total_sale", "sum")
).sort_values("total_revenue", ascending=False)

print("\nProduct Summary:")
print(product_summary)

# Save to JSON
product_summary.to_json("sales_summary.json")
```

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Pandas se CSV load karo, first 5 rows print karo.
2. **(Basic)** Numeric column ka average calculate karo.
3. **(Medium)** Filter rows where column > threshold, result JSON mein save karo.
4. **(Medium)** Group by category, sum of values in each group.
5. **(Hard)** Do CSV files load karo, merge karo, merged data JSON mein export karo.