from fastapi import FastAPI, HTTPException, Query, status
from enum import Enum
from pydantic import BaseModel, Field

app = FastAPI()

# ==================== BASIC ROUTE ====================
@app.get("/")
def home():
    return {"message": "Hello FirstAPI"}

# ==================== PATH PARAMETERS ====================
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

# ==================== HTTP METHODS (CRUD) ====================
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"action": "fetch", "product_id": product_id}

@app.post("/products/")
def create_product(name: str):
    return {"action": "create", "name": name}

@app.put("/products/{product_id}")
def update_product(product_id: int, name: str):
    return {"action": "update", "product_id": product_id, "name": name}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {"action": "delete", "product_id": product_id}

# ==================== MULTIPLE PATH PARAMETERS ====================
@app.get("/users/{user_name}/rollnos/{roll_no}")
def get_rollno(user_name: str, roll_no: int):
    return {"user_name": user_name, "roll_no": roll_no}

# ==================== PATH PARAM WITH ENUM ====================
class Role(str, Enum):
    admin = "admin"
    user = "user"
    developer = "developer"

@app.get("/users/{user_id}/roles/{role}")
def get_user_role(user_id: int, role: Role):
    return {"user_id": user_id, "role": role}

# ==================== QUERY PARAMETERS ====================

# 1. Basic Query Params (Required)
@app.get("/items/basic/")
def get_items_basic(skip: int, limit: int):
    return {"skip": skip, "limit": limit}

# 2. Optional Query Params (Default values)
@app.get("/items/optional/")
def get_items_optional(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}

# 3. Validated Query Params (with Query())
@app.get("/items/validated/")
def get_items_validated(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(
        None,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\s]+$"
    )
):
    return {"skip": skip, "limit": limit, "search": search}

# ==================== REQUIRED QUERY PARAM WITH VALIDATION ====================
@app.get("/search/")
def search_items(q: str = Query(..., min_length=3)):
    return {"query": q}

# ==================== REQUEST BODY + PYDANTIC MODELS ====================
class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)
    description: str | None = Field(None, max_length=200)
    tags: list[str] = []

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}

# ==================== BODY + PATH + QUERY — EK SAATH ====================
@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    q: str | None = None,
    update_all: bool = False
):
    return {
        "item_id": item_id,
        "query": q,
        "updated_data": item,
        "full_update": update_all
    }

# ==================== RESPONSE MODELS & STATUS CODES ====================
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "password": user.password  # response_model filter karega
    }

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item2(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return

# ==================== CHAPTER 1 EXERCISE - STUDENT MANAGEMENT API ====================
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=5, le=30)
    grade: str = Field(..., min_length=1)

class StudentResponse(StudentCreate):
    id: int

students_db = []
next_id = 1

@app.post("/students/", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    global next_id
    new_student = StudentResponse(id=next_id, **student.model_dump())
    students_db.append(new_student)
    next_id += 1
    return new_student

@app.get("/students/")
def get_students(skip: int = 0, limit: int = Query(10, le=100)):
    return students_db[skip : skip + limit]

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students_db:
        if s.id == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")

@app.put("/students/{student_id}")
def update_student(student_id: int, data: StudentCreate):
    for i, s in enumerate(students_db):
        if s.id == student_id:
            students_db[i] = StudentResponse(id=student_id, **data.model_dump())
            return students_db[i]
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    for i, s in enumerate(students_db):
        if s.id == student_id:
            students_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Student not found")