# JSON & CSV — ML ke Data Formats

## Simple Explanation (Hinglish)
ML models ke saath kaam karte waqt, data mostly **JSON** ya **CSV** format mein milta hai:
- **CSV**: Excel sheet jaisa — rows aur columns. Jaise `name,age,salary`
- **JSON**: Dictionary jaisa structure. Jaise `{"name": "Rahul", "age": 25}`

Training data, API responses, model configurations — sab kuch inhi formats mein hota hai. Inhe padhna-likhna seekhna **ML integration ke liye must hai**.

## Theory
- **CSV** (Comma Separated Values): Tabular data, har line ek row, columns comma se separated
- **JSON** (JavaScript Object Notation): Key-value pairs, nested structure support karta hai
- Python mein `csv` aur `json` modules built-in aate hain — kuch install nahi karna padta

## Examples

```python
# ===== CSV Examples =====
import csv

# CSV file read karna
with open("students.csv", "r") as file:
    reader = csv.reader(file)
    headers = next(reader)  # Pehli line = header
    for row in reader:
        print(f"Name: {row[0]}, Age: {row[1]}")

# CSV as Dictionary (recommended for ML)
with open("students.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["name"], row["marks"])  # Column name se access

# CSV file write karna
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "age", "city"])  # Header
    writer.writerow(["Rahul", 25, "Delhi"])
    writer.writerow(["Priya", 22, "Mumbai"])


# ===== JSON Examples =====
import json

# Python dict → JSON string
data = {"name": "Rahul", "scores": [85, 90, 78], "active": True}
json_str = json.dumps(data, indent=2)  # Pretty print
print(json_str)

# JSON string → Python dict
json_data = '{"name": "AI Model", "version": 2.0, "accuracy": 0.95}'
parsed = json.loads(json_data)
print(parsed["name"])  # AI Model

# JSON file read/write
with open("config.json", "w") as f:
    json.dump({"model": "regression", "lr": 0.01}, f, indent=2)

with open("config.json", "r") as f:
    config = json.load(f)
    print(config["model"])  # regression


# ===== ML Dataset Example =====
import csv
import json

# CSV data ko list of dicts mein convert karo (ML model ke liye)
def load_csv_to_dicts(filepath):
    with open(filepath, "r") as f:
        return list(csv.DictReader(f))

# Dicts ko JSON mein save karo (processed data)
def save_as_json(data, filepath):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# Usage
students = load_csv_to_dicts("students.csv")
save_as_json(students, "students_processed.json")
```

## Dry Run
`json.dumps({"name": "test", "score": 95.5}, indent=2)`:
```
Step 1: Python dict → JSON string conversion
Step 2: indent=2 → har nested level pe 2 spaces add karega
Result:
{
  "name": "test",
  "score": 95.5
}
```

## Common Mistakes
1. **CSV with commas in data**: `"Delhi, India"` — quotes mein wrap karo
2. **JSON key without quotes**: `{name: "Rahul"}` ❌. Python dict mein allowed hai, JSON string mein nahi
3. **Forgetting `newline=""` in CSV write**: Extra blank lines aa jati hain
4. **JSON double quotes**: Single quotes ❌, sirf double quotes ✅ JSON mein

## Interview Notes
1. **`pd.read_csv()` is faster** than `csv` module for large datasets (Pandas)
2. **JSON vs CSV**: JSON nested data handle karta hai, CSV flat/tabular ke liye
3. **ML pipeline**: Raw data (CSV) → Cleaned data (JSON) → Features (NumPy array) → Model

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** CSV file read karo using csv.reader aur rows print karo.
2. **(Basic)** Dict to JSON string convert karo using json.dumps().
3. **(Medium)** CSV mein se marks > 80 wale students ki list print karo.
4. **(Medium)** Function likho jo list of dicts ko JSON file mein save kare.
5. **(Hard)** Do CSV files ko merge karo aur JSON mein save karo.