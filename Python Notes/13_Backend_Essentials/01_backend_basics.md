# Backend Basics — Flask/FastAPI se API Banana

## Simple Explanation (Hinglish)
Backend ek **server** hota hai jo **requests** sunta hai aur **responses** bhejta hai. Jaise:
- App ne "mujhe user data chahiye" kaha → Backend ne database se data laakar diya
- App ne "yeh photo analyze karo" kaha → Backend ne ML model chalaya aur result diya

**API** (Application Programming Interface) ek **waiter** ki tarah hai — user (frontend) aur backend ke beech mein baat karata hai.

## Theory
- **Flask**: Simple, lightweight backend framework (chhote projects, quick prototypes)
- **FastAPI**: Modern, fast, automatic docs (production-ready, ML APIs ke liye best)
- **REST API**: HTTP methods use karta hai — GET (data lena), POST (data bhejna), PUT (update), DELETE (hataana)
- **JSON**: API response ka standard format

## Examples

### 1. Flask — Simple API

```python
# pip install flask
from flask import Flask, request, jsonify

app = Flask(__name__)

# GET request — data lena
@app.route("/", methods=["GET"])
def home():
    return {"message": "Hello, API is working!"}

# GET with parameter
@app.route("/user/<name>", methods=["GET"])
def get_user(name):
    return {"name": name, "status": "active"}

# POST request — data bhejna (ML ke liye important)
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()  # JSON input lo
    value = data.get("value", 0)
    prediction = value * 2  # Simple logic (actual ML model yahan aayega)
    return jsonify({"input": value, "prediction": prediction})

# Run: python app.py
if __name__ == "__main__":
    app.run(debug=True)
```

### 2. FastAPI — Modern ML API

```python
# pip install fastapi uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML API")

# Request model (input ka format define karo)
class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float = 0.0  # Default value

class PredictionOutput(BaseModel):
    prediction: float
    probability: float

# GET — health check
@app.get("/")
def read_root():
    return {"status": "ML API is running"}

# POST — ML prediction endpoint
@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    # Yahan actual ML model chalega
    result = data.feature1 * 0.5 + data.feature2 * 0.3 + data.feature3 * 0.2
    return PredictionOutput(prediction=result, probability=0.85)

# POST — file upload (image classification ke liye)
from fastapi import UploadFile, File
import shutil
import os

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Save uploaded file
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Yahan image classification model chalega
    return {"filename": file.filename, "size": file.size, "prediction": "cat"}

# Run: uvicorn app:app --reload
# Automatic docs: http://localhost:8000/docs
```

### 3. ML Model Integration Example

```python
# backend_ml_api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib  # ML model load karne ke liye
import numpy as np

app = FastAPI()

# Load trained model
# model = joblib.load("model.pkl")

class Features(BaseModel):
    age: float
    salary: float
    experience: float

@app.post("/predict-salary")
def predict_salary(features: Features):
    # Convert to numpy array for model
    input_array = np.array([[features.age, features.salary, features.experience]])
    
    # Actual prediction (abhi dummy)
    # prediction = model.predict(input_array)
    prediction = features.age * 0.1 + features.salary * 0.05
    
    return {"predicted_salary": round(prediction, 2)}

@app.get("/model-info")
def model_info():
    return {
        "model": "Salary Predictor v1.0",
        "features": ["age", "salary", "experience"],
        "accuracy": 0.92
    }
```

## Common Mistakes
1. **CORS error**: Frontend alag port pe hai toh CORS enable karna bhoolna
2. **Not using POST for predictions**: GET requests mein data URL mein dikhta hai. POST use karo
3. **Not validating input**: User kuch bhi bhej sakta hai. `pydantic` models validation ke liye best hai
4. **Forgetting error handling**: Hamesha try-except use karo API mein

## Interview Notes
1. **Flask vs FastAPI**: Flask simple hai, FastAPI faster hai + automatic docs + validation
2. **ML deployment pattern**: Model pickle (.pkl) ya ONNX format mein save karo, FastAPI se load karo
3. **Async endpoints**: FastAPI async support karta hai — isse ML inference block nahi karta

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Flask app banao with GET /hello returning {"message":"Hello World"}.
2. **(Basic)** FastAPI GET /ping returning {"status":"ok"}.
3. **(Medium)** FastAPI POST endpoint jo number ka square return kare.
4. **(Medium)** Flask API with addition aur multiplication endpoints.
5. **(Hard)** FastAPI app jo .pkl model load kare aur /predict serve kare.