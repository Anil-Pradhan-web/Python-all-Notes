# ML Integration Projects — Python se Model Deploy

## Simple Explanation (Hinglish)
ML model banana (training) aur model ko **use karna** (inference) — dono alag cheezein hain. Tujhe seekhna hai ki trained model ko kaise load karo, usse prediction lo, aur API ke through deploy karo.

## Project 1: Simple ML Model Load + Predict 🤖
```python
# Simulate a trained model (actually yeh simple math hai)
# Real project mein: import joblib; model = joblib.load("model.pkl")

import json
import numpy as np

# Dummy ML model class
class SimpleModel:
    def __init__(self):
        self.weights = {"feature1": 0.5, "feature2": 0.3, "feature3": 0.2}
        self.bias = 10
    
    def predict(self, features: list) -> float:
        """Simple linear regression prediction"""
        result = self.bias
        for i, f in enumerate([f"feature{i+1}" for i in range(len(features))]):
            result += features[i] * self.weights.get(f, 0)
        return result

# Model load karo
model = SimpleModel()

# Input data (jo user se aayega)
input_data = {"feature1": 25, "feature2": 50000, "feature3": 2}
features = [input_data["feature1"], input_data["feature2"], input_data["feature3"]]

# Prediction lo
prediction = model.predict(features)

# Result save karo
result = {
    "input": input_data,
    "prediction": round(prediction, 2),
    "confidence": 0.92
}

with open("prediction_result.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"✅ Prediction saved: ₹{result['prediction']:,.2f}")
```

## Project 2: CSV Data → Model → API Pipeline 🔄
```python
# Complete pipeline: CSV data load → preprocess → model predict → API serve
import pandas as pd
import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Step 1: Load and preprocess data
def load_and_preprocess(csv_path):
    df = pd.read_csv(csv_path)
    # Handle missing values
    df = df.fillna(df.mean())
    return df

# Step 2: Simple model class
class HousePriceModel:
    def predict(self, area, bedrooms, age):
        # Dummy formula (real model yahan aayega)
        return (area * 5000) + (bedrooms * 200000) - (age * 10000)

model = HousePriceModel()

# Step 3: API endpoint
class HouseFeatures(BaseModel):
    area: float
    bedrooms: int
    age: int

@app.post("/predict-house-price")
def predict_price(features: HouseFeatures):
    prediction = model.predict(features.area, features.bedrooms, features.age)
    return {
        "price": round(prediction, 2),
        "currency": "INR",
        "features": features
    }

# Step 4: Batch prediction from file
@app.post("/batch-predict")
def batch_predict(file_path: str = "houses.csv"):
    df = load_and_preprocess(file_path)
    predictions = []
    for _, row in df.iterrows():
        pred = model.predict(row["area"], row["bedrooms"], row["age"])
        predictions.append({"area": row["area"], "price": round(pred, 2)})
    
    with open("batch_results.json", "w") as f:
        json.dump(predictions, f, indent=2)
    
    return {"total": len(predictions), "results": predictions[:5]}
```

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Function likho jo 3 numbers ka weighted sum return kare.
2. **(Basic)** Model prediction result (dict) ko JSON mein save karo.
3. **(Medium)** CSV load karo, har row pe prediction run karo, results JSON mein save karo.
4. **(Medium)** FastAPI endpoint /predict banao jo features accept kare aur prediction return kare.
5. **(Hard)** Pipeline banao: CSV -> pandas preprocess -> model predict -> FastAPI serve -> JSON output.