# 📘 Chapter 1: FastAPI Basics

> FastAPI ka foundation — yeh samajh liya toh baaki sab easy hai.

---

## 🔰 FastAPI Kya Hai?

FastAPI ek **modern, high-performance Python web framework** hai jo APIs banana ke liye use hota hai.

**Kyun use karein?**
- ⚡ **Super fast** — Node.js aur Go ke level ki performance
- 📝 **Auto documentation** — Swagger UI free mein milta hai
- ✅ **Type-safe** — Python type hints use karta hai (Pydantic)
- 🧩 **Async support** — built-in async/await

```bash
# Installation
pip install fastapi uvicorn[standard]
```

---

## 1.1 🚀 Pehla FastAPI App

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}
```

**Run karo:**
```bash
uvicorn main:app --reload
```

- `main` → file name (main.py)
- `app` → FastAPI instance
- `--reload` → code change pe auto restart (development ke liye)

💡 **Pro Tip:** Browser mein `http://127.0.0.1:8000/docs` pe jaao — Swagger UI dikhai dega!

---

## 1.2 📌 Path Operations (HTTP Methods)

FastAPI mein 4 main HTTP methods hain — yeh RESTful API ka backbone hai:

| Method | Use | Decorator |
|--------|-----|-----------|
| GET | Data fetch karna | `@app.get()` |
| POST | Naya data banana | `@app.post()` |
| PUT | Poora data update karna | `@app.put()` |
| PATCH | Partial update | `@app.patch()` |
| DELETE | Data delete karna | `@app.delete()` |

### ✅ Example: Complete CRUD

```python
from fastapi import FastAPI

app = FastAPI()

# In-memory database (practice ke liye)
items_db = {}

# CREATE
@app.post("/items/")
def create_item(name: str, price: float):
    item_id = len(items_db) + 1
    items_db[item_id] = {"name": name, "price": price}
    return {"id": item_id, "item": items_db[item_id]}

# READ - sabhi items
@app.get("/items/")
def get_all_items():
    return items_db

# READ - ek item
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Item not found"}
    return items_db[item_id]

# UPDATE
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    if item_id not in items_db:
        return {"error": "Item not found"}
    items_db[item_id] = {"name": name, "price": price}
    return {"message": "Updated", "item": items_db[item_id]}

# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Item not found"}
    deleted = items_db.pop(item_id)
    return {"message": "Deleted", "item": deleted}
```

---

## 1.3 🛤️ Path Parameters

Path parameters URL ka part hote hain — dynamic values pass karne ke liye.

```python
# Basic path parameter
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
# URL: /users/42 → {"user_id": 42}
```

### Multiple Path Parameters

```python
@app.get("/companies/{company_id}/employees/{emp_id}")
def get_employee(company_id: int, emp_id: int):
    return {
        "company_id": company_id,
        "employee_id": emp_id
    }
# URL: /companies/1/employees/5
```

### Path Parameter with Validation (Enum)

```python
from enum import Enum

class Department(str, Enum):
    engineering = "engineering"
    marketing = "marketing"
    hr = "hr"

@app.get("/departments/{dept_name}")
def get_department(dept_name: Department):
    return {"department": dept_name}
# Sirf allowed values accept karega — baaki pe 422 error
```

> ⚠️ **Common Mistake:** Path parameter ka type hint mat bhoolo! Agar `int` likha toh FastAPI automatically validate karega. Bina type hint ke sab `str` maana jaata hai.

---

## 1.4 🔍 Query Parameters

Query parameters URL ke `?` ke baad aate hain — filtering/searching ke liye.

```python
@app.get("/products/")
def get_products(skip: int = 0, limit: int = 10, category: str | None = None):
    # URL: /products/?skip=0&limit=5&category=electronics
    result = {
        "skip": skip,
        "limit": limit,
    }
    if category:
        result["category"] = category
    return result
```

### Required vs Optional Query Params

```python
# ✅ Required — default value nahi diya
@app.get("/search/")
def search(q: str):  # q dena zaroori hai
    return {"query": q}

# ✅ Optional — default value diya ya None
@app.get("/search2/")
def search2(q: str | None = None):  # q optional hai
    return {"query": q}
```

### Query Param Validation (with `Query`)

```python
from fastapi import Query

@app.get("/items/")
def get_items(
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z]+$",  # sirf letters
        title="Search Query",
        description="Search ke liye query string"
    )
):
    return {"q": q}
```

💡 **Pro Tip:** `Query()` use karo jab validation chahiye — ye Swagger docs mein bhi dikhta hai!

---

## 1.5 📦 Request Body (Pydantic Models)

POST/PUT requests mein data body mein bhejte hain. FastAPI Pydantic models use karta hai.

```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_available: bool = True

@app.post("/items/")
def create_item(item: Item):
    return {
        "message": f"Item '{item.name}' created!",
        "item": item.model_dump()  # Pydantic v2
    }
```

**Request Body (JSON):**
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 75000.0,
    "is_available": true
}
```

### Body + Path + Query — Ek Saath

```python
@app.put("/items/{item_id}")
def update_item(
    item_id: int,        # Path parameter
    item: Item,          # Request body
    q: str | None = None # Query parameter
):
    result = {"item_id": item_id, "item": item.model_dump()}
    if q:
        result["q"] = q
    return result
```

> FastAPI automatically samajhta hai:
> - Function parameter jo **path mein hai** → Path parameter
> - Function parameter jo **Pydantic model hai** → Request body
> - **Baaki sab** → Query parameters

---

## 1.6 📤 Response Models & Status Codes

### Response Model — Control karo kya return ho

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # ❌ password nahi bhejenge response mein!

@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    # DB mein save karo (simulate)
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "password": user.password  # yeh filter ho jaayega!
    }
```

💡 **Pro Tip:** `response_model` use karo sensitive data (password, tokens) filter karne ke liye.

### Status Codes

```python
from fastapi import FastAPI, status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return  # 204 = No Content
```

**Common Status Codes:**

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Default GET response |
| 201 | Created | POST — naya resource bana |
| 204 | No Content | DELETE success |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Login required |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource nahi mila |
| 422 | Unprocessable Entity | Validation error (FastAPI default) |
| 500 | Internal Server Error | Server crash |

---

## 1.7 🔄 Multiple Response Types

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail=f"Item with id {item_id} not found"
        )
    return items_db[item_id]
```

### Custom Response Headers

```python
from fastapi.responses import JSONResponse

@app.get("/custom/")
def custom_response():
    content = {"message": "Hello with custom headers!"}
    headers = {"X-Custom-Header": "my-value"}
    return JSONResponse(content=content, headers=headers)
```

---

## ⚠️ Common Mistakes (Beginners)

| # | Mistake | Solution |
|---|---------|----------|
| 1 | Path order galat — `/users/me` ke pehle `/users/{user_id}` | Fixed paths pehle likho, dynamic baad mein |
| 2 | Type hint nahi diya | Hamesha type hint do — validation free milti hai |
| 3 | `return` mein dict nahi diya | FastAPI dict, Pydantic model, ya list return karta hai |
| 4 | `uvicorn` mein `--reload` production mein use kiya | `--reload` sirf development ke liye! |
| 5 | Request body ke liye plain `dict` use kiya | Pydantic `BaseModel` use karo — validation milegi |

---

## 🎯 Practice Exercise

Ek **Student Management API** banao:

1. `POST /students/` — Create student (name, age, grade)
2. `GET /students/` — All students (with skip & limit)
3. `GET /students/{student_id}` — Single student
4. `PUT /students/{student_id}` — Update student
5. `DELETE /students/{student_id}` — Delete student

**Bonus:**
- Response model mein `id` add karo
- Proper status codes use karo
- Age 5-30 ke beech validate karo

---

> **Next Chapter:** [02 — Pydantic (Data Validation Ka Raja)](./02_pydantic.md) →
