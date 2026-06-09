# 🗓️ FastAPI 21-Day Study Plan (Hinglish)

> **Goal:** Hafte mein 6 din padho, 7th day rest ya revision.
> **Time:** Roz 1-1.5 ghanta (code likhke + run karke)
> **Mantra:** "Type karo, Copy-Paste mat karo!"

---

## 🟢 Week 1: Foundation (Day 1-6)

### Day 1 — FastAPI Setup + Pehla App 🚀
**Read:** Chapter 1 (sirf 1.1 - Pehla FastAPI App)
**Time:** 1 hour

**Steps:**
1. Install Python 3.10+ (agar nahi hai toh)
2. Terminal mein run karo:
   ```bash
   pip install fastapi uvicorn[standard]
   ```
3. Naya folder banao: `C:\Users\ANIL\Desktop\fastapi-practice`
4. `main.py` banao aur yeh code likho:
   ```python
   from fastapi import FastAPI
   app = FastAPI()
   
   @app.get("/")
   def home():
       return {"message": "Hello FastAPI!"}
   ```
5. Run karo:
   ```bash
   uvicorn main:app --reload
   ```
6. Browser mein kholo: `http://127.0.0.1:8000`
7. Swagger UI dekho: `http://127.0.0.1:8000/docs`

**✅ Goal achieved:** Terminal mein `uvicorn` chal raha hai, browser mein JSON dikh raha hai.

---

### Day 2 — Path aur Query Parameters 🛤️
**Read:** Chapter 1.2 to 1.4
**Time:** 1-1.5 hours

**Steps:**
1. `main.py` mein 5 naye endpoints add karo:
   - `GET /users/{user_id}` → path param
   - `GET /products/?skip=0&limit=10` → query params
   - `GET /search/?q=` → required query param
   - `GET /items/validated/` → validated query params (min_length, pattern)
   - `GET /departments/{dept_name}` → enum validation

**Code练习:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "message": f"User {user_id} found"}

@app.get("/products/")
def get_products(skip: int = 0, limit: int = 10, category: str | None = None):
    return {"skip": skip, "limit": limit, "category": category}
```

**Test karo:** Swagger UI mein `/products/?skip=5&limit=20&category=electronics` try karo.

**⚡ Challenge:** Ek endpoint banao `GET /calculator/?a=10&b=5&operation=add` jo do numbers add kare.

---

### Day 3 — Request Body + Pydantic Models 📦
**Read:** Chapter 1.5 + 1.6
**Time:** 1-1.5 hours

**Steps:**
1. Chapter 1.5 ka code likho — `Item` model banake POST `/items/` endpoint
2. Response model use karo — `UserCreate` vs `UserResponse` (password filter)
3. Status codes use karo — `status_code=201`, `status_code=204`

**Important:** Yeh samjho ki FastAPI kaise automatically decide karta hai:
- Path mein hai → path param
- Pydantic model hai → request body
- Baki sab → query param

**✅ Test karo:** Swagger mein POST `/items/` pe JSON body bhejo.

---

### Day 4 — Pydantic Deep Dive 🎯
**Read:** Chapter 2 (poora)
**Time:** 1.5 hours

**Sirf yeh concepts code karo (baaki theory padho):**
1. ✅ `BaseModel` — basic model
2. ✅ `Field()` — validations (min_length, gt, le, pattern)
3. ✅ Nested models — Address inside User
4. ✅ `@field_validator` — custom validation (email format, age range)
5. ✅ `@model_validator` — password match check

**Code练习: Nested Model Example**
```python
from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    pin_code: str = Field(pattern=r"^\d{6}$")

class User(BaseModel):
    name: str
    age: int = Field(ge=18, le=100)
    address: Address
```

**⚡ Challenge:** Ek `Order` model banao jismein `items: list[Item]` ho aur `total_price` auto-calculate ho.

---

### Day 5 — Dependency Injection + Middleware ⚡
**Read:** Chapter 3 (3.1, 3.4)
**Time:** 1.5 hours

**Sirf yeh 2 concepts:**
1. **Dependency Injection** (`Depends`) — Chapter 3.1
2. **Middleware** — Chapter 3.4

**Code练习:**
```python
# Dependency for common pagination
from fastapi import Depends, Query

def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def get_items(pg=Depends(pagination)):
    return pg

# Middleware for timing
import time
@app.middleware("http")
async def add_timing(request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

**Mistake yaad rakho:** `Depends(get_db)` — brackets nahi lagane! ❌ `Depends(get_db())`

---

### Day 6 — CORS + File Uploads + Error Handling 🌐
**Read:** Chapter 3 (3.3, 3.5, 3.6)
**Time:** 1.5 hours

**3 cheezein code karo:**
1. **CORS setup** — frontend se connect karte waqt kaam aayega
2. **File upload** — `UploadFile` use karo
3. **Error handling** — `HTTPException` + custom exception handler

**Code练习:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**✅ Week 1 Complete!** Ab tak FastAPI basics clear ho gaye hain.

---

## 🟡 Week 2: Intermediate (Day 7-12)

### Day 7 — REST 😴
**Aaj kuch mat padho!**
- Pichle 6 din ka revision karo
- Jo code likha tha wapas dekho
- Agar koi doubt hai toh YouTube pe "FastAPI basics" search karo

---

### Day 8 — Database Setup (SQLAlchemy) 🗄️
**Read:** Chapter 4 (4.1, 4.2, 4.3)
**Time:** 1.5 hours

**Steps:**
1. Install: `pip install sqlalchemy`
2. `database.py` banao — engine + session + get_db
3. `models.py` banao — `User` table
4. `schemas.py` banao — `UserCreate`, `UserResponse`

**Main concept:** SQLAlchemy model ↔ Pydantic schema ka relationship samjho.

---

### Day 9 — Database CRUD Operations ✍️
**Read:** Chapter 4 (4.4, 4.5)
**Time:** 1.5 hours

**Code练习:**
1. `crud.py` banao — create_user, get_user, get_users
2. Router mein CRUD endpoints banao
3. Postman ya Swagger se test karo

**Mistake yaad rakho:** CREATE/UPDATE/DELETE ke baad `db.commit()` karna mat bhoolna!

---

### Day 10 — Alembic Migrations 🔄
**Read:** Chapter 4 (4.6)
**Time:** 1 hour

```bash
pip install alembic
alembic init alembic
# env.py configure karo
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

**✅ Goal:** `alembic upgrade head` chal raha hai, table ban gaya hai.

---

### Day 11 — JWT Authentication 🔐
**Read:** Chapter 5 (5.1 to 5.4)
**Time:** 1.5 hours

**Steps:**
1. Install: `pip install python-jose[cryptography] passlib[bcrypt] python-multipart`
2. `security.py` banao:
   - `hash_password()`
   - `verify_password()`
   - `create_access_token()`
   - `verify_token()`

**Code练习:**
```python
token = create_access_token({"sub": "test@email.com"})
print(token)  # JWT token dikhega

payload = verify_token(token)
print(payload)  # Wapas data milega
```

---

### Day 12 — Login + Register + Protected Routes 🔒
**Read:** Chapter 5 (5.5, 5.6)
**Time:** 1.5 hours

**Steps:**
1. `/auth/register` endpoint — password hash karke DB mein save
2. `/auth/login` endpoint — password verify karke JWT return
3. `/users/me` endpoint — token se current user nikaalo (protected)
4. Swagger mein "Authorize" button se token set karo

**⚡ Challenge:** Admin aur user roles implement karo (RBAC).

**✅ Week 2 Complete!** Database + Auth — real app ka backbone aa gaya.

---

## 🔴 Week 3: Advanced + Project (Day 13-21)

### Day 13 — Advanced Async + WebSockets ⚡
**Read:** Chapter 6 (6.1, 6.2)
**Time:** 1.5 hours

**Sirf itna karo:**
1. `async def` vs `def` ka difference samjho
2. WebSocket echo server banao
3. `http://localhost:8000/ws` — browser se connect karo

**Important Rule:** `async def` mein kabhi `time.sleep()` mat use karo! `await asyncio.sleep()` use karo.

---

### Day 14 — Background Tasks + Lifespan 🔄
**Read:** Chapter 6 (6.3, 6.4 basics)
**Time:** 1 hour

**Background Tasks:**
```python
from fastapi import BackgroundTasks

def send_email(email: str):
    print(f"Email sent to {email}")

@app.post("/register/")
def register(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_email, email)
    return {"message": "Registered"}
```

---

### Day 15 — Swagger + API Docs Customization 📝
**Read:** Chapter 7
**Time:** 1 hour

**Code练习:**
1. `tags` use karo endpoints organize karne ke liye
2. Response examples do
3. `include_in_schema=False` se internal endpoints hide karo

---

### Day 16 — LLM Integration 🤖
**Read:** Chapter 8 (8.1, 8.2)
**Time:** 1.5 hours

**Sirf itna karo:**
1. OpenAI API key lo (ya kisi free LLM ka)
2. Simple chat endpoint banao — prompt bhejo, response pao
3. Streaming response banao (optional)

**Agar API key nahi hai toh skip karo, baad mein dekhna.**

---

### Day 17 — Security + Performance 🔒⚡
**Read:** Chapter 9 + Chapter 10
**Time:** 1.5 hours

**Sirf yeh concepts padho:**
- Chapter 9: API keys, `.env` secrets management
- Chapter 10: Redis caching concept, GZip compression

**Code练习:** `config.py` banao pydantic-settings ke saath.

---

### Day 18 — Testing + Docker 🧪🐳
**Read:** Chapter 11 (11.1, 11.2)
**Time:** 1.5 hours

**Code练习:**
1. Pytest test likho — `test_main.py`
2. Dockerfile banao — `docker build .`
3. Docker run karo

---

### Day 19 — Project Structure (CRITICAL CHAPTER) 🏗️
**Read:** Chapter 13 (POORA)
**Time:** 1.5 hours

**Yeh chapter SABSE IMPORTANT hai!** 

**Samajhne wali baatein:**
- Router thin → Service mein logic → Repository mein DB
- Config management
- Custom exceptions

**Folder structure banao:**
```
app/
├── main.py
├── config.py
├── database.py
├── models/
├── schemas/
├── routers/
├── services/
├── repositories/
├── dependencies/
└── exceptions/
```

---

### Day 20 — Mini Project 🚀 (PART 1)
**Read:** Chapter 14 (setup + models + schemas + auth)
**Time:** 2 hours

Folder banao `ai-blog-api/` aur chapter 14 ka code likho:
1. `config.py` + `database.py`
2. Models (User, Post)
3. Schemas (Create, Update, Response)
4. Auth register/login

---

### Day 21 — Mini Project 🚀 (PART 2) + Celebration 🎉
**Read:** Chapter 14 (remaining)
**Time:** 2 hours

1. Posts CRUD endpoints
2. AI summary endpoint
3. Sab kuch run karo
4. Swagger UI mein test karo

```
POST /auth/register → User banao
POST /auth/login → Token lo
POST /posts/ → Blog post likho (token ke saath)
GET /posts/ → Sab posts dekho
POST /ai/summarize/1 → AI summary banao
```

**🎉 Congratulations! Ab tu FastAPI backend developer hai!**

**Bonus:** Chapter 15 (Backend Checklist) aur Chapter 16 (AI Era) padho — mindset ke liye.

---

## 📋 Quick Reference (Har Din Ke Liye)

```
Roz ka routine:
1. Chapter padho (20-30 min)
2. Code likho (30-40 min) — khud type karo, copy-paste nahi!
3. Run karo (5-10 min) — error aaye toh debug karo
4. Swagger UI mein test karo (5 min)
```

**Kuch rules:**
- ❌ Copy-paste mat karo — type karo, samjh aaega
- ❌ Ek din skip mat karo — 3 hafte hi hai
- ✅ Error aaye toh ghabrana nahi — error ko Google karo
- ✅ Doubt ho toh ChatGPT se pucho: "FastAPI mein X kaise karte hain?"

## 🎯 Final Goal (21 din baad)

Tu yeh sab kar payega:
- FastAPI app bana aur run kar paayega
- Database se connect kar paayega (SQLite/PostgreSQL)
- JWT authentication laga paayega (login/register)
- CRUD APIs bana paayega
- Docker mein app daal paayega
- Mini project complete kar paayega

---

> **Mantra:** "Code likh, run kar, error dekh, fix kar — yahi seekhne ka tarika hai."