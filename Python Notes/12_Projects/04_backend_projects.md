# Backend Projects — Real APIs Banao

## Simple Explanation (Hinglish)
Ab tujhe aata hai: Python basics, OOP, file handling, JSON/CSV, aur FastAPI. Ab in sabka **combination** bana — real-world backend projects.

## Project 1: Todo API with JSON Storage ✅
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()
DATA_FILE = "todos.json"

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

def load_todos():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)

@app.get("/todos")
def get_all():
    return load_todos()

@app.post("/todos")
def create(todo: Todo):
    todos = load_todos()
    todos.append(todo.model_dump())
    save_todos(todos)
    return {"message": "Todo created", "todo": todo}

@app.delete("/todos/{todo_id}")
def delete(todo_id: int):
    todos = load_todos()
    todos = [t for t in todos if t["id"] != todo_id]
    save_todos(todos)
    return {"message": "Deleted"}
```

## Project 2: CSV Upload + Analysis API 📊
```python
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import json
import shutil
from pathlib import Path

app = FastAPI()
UPLOAD_DIR = "uploads/"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    # Save uploaded file
    filepath = Path(UPLOAD_DIR) / file.filename
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Analyze
    df = pd.read_csv(filepath)
    summary = {
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
        "numeric_stats": df.describe().to_dict() if not df.empty else {}
    }
    
    # Save summary
    with open("analysis_result.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    return summary

@app.get("/results")
def get_results():
    if Path("analysis_result.json").exists():
        with open("analysis_result.json") as f:
            return json.load(f)
    return {"message": "No analysis results yet"}
```

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** FastAPI app banao with GET /hello returning {"message":"Hello World"}.
2. **(Basic)** GET /square/{num} endpoint banao jo square return kare.
3. **(Medium)** Todo API banao: GET all, POST new, DELETE by id (in-memory list).
4. **(Medium)** File upload endpoint banao jo CSV save kare aur file info return kare.
5. **(Hard)** CSV analyzer API: upload -> detect column types -> calculate stats -> return JSON.