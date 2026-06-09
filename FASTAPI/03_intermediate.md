# 📘 Chapter 3: Intermediate Concepts

> Ab real-world FastAPI seekhte hain — Dependency Injection, Middleware, File Uploads, CORS, aur Error Handling.

---

## 3.1 ⭐ Dependency Injection (Depends) — SUPER IMPORTANT

> Yeh FastAPI ka sabse powerful feature hai. Ek baar samajh gaye toh sab clean ho jaayega.

**Dependency Injection (DI) kya hai?**
Ek function jo doosre function ko kuch "provide" karta hai — jaise DB connection, current user, ya koi common logic.

### Basic Example

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# Dependency function
def get_db():
    """Fake DB connection provide karta hai"""
    db = {"connection": "active"}
    print("DB connected!")
    yield db  # yield = DI with cleanup
    print("DB disconnected!")  # cleanup code

# Route mein use karo
@app.get("/items/")
def get_items(db=Depends(get_db)):
    return {"db_status": db["connection"], "items": []}
```

### Real-World: Common Query Params

```python
from fastapi import Query

# Har listing endpoint pe same params chahiye
def common_pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    order: str = Query(default="desc", pattern="^(asc|desc)$")
):
    return {"skip": skip, "limit": limit, "sort_by": sort_by, "order": order}

@app.get("/users/")
def get_users(pagination=Depends(common_pagination)):
    return {"pagination": pagination, "users": []}

@app.get("/products/")
def get_products(pagination=Depends(common_pagination)):
    return {"pagination": pagination, "products": []}

# ✅ DRY principle — same code repeat nahi karna padta!
```

### Chained Dependencies

```python
def get_db():
    db = FakeDB()
    yield db

def get_current_user(db=Depends(get_db)):
    """DB se current user nikaalo"""
    user = db.get_user(token="...")
    return user

def get_admin_user(current_user=Depends(get_current_user)):
    """Check karo admin hai ya nahi"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Route — sirf admin access kar sakte hain
@app.delete("/users/{user_id}")
def delete_user(user_id: int, admin=Depends(get_admin_user)):
    return {"message": f"User {user_id} deleted by {admin.name}"}
```

### Class-Based Dependencies

```python
class Paginator:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
def get_items(paginator: Paginator = Depends()):
    # Depends() bina argument ke = class ko Depends mein wrap karta hai
    return {"skip": paginator.skip, "limit": paginator.limit}
```

> 💡 **Pro Tip:** Depends ke andar Depends chain kar sakte ho. FastAPI automatically resolve karta hai — yeh **Dependency Tree** kehlata hai.

---

## 3.2 🔄 Background Tasks

Heavy kaam ko background mein bhej do — user ko turant response do.

```python
from fastapi import BackgroundTasks

def send_email(email: str, subject: str, body: str):
    """Yeh function background mein chalega"""
    import time
    time.sleep(5)  # Simulate email sending
    print(f"Email sent to {email}: {subject}")

def write_log(message: str):
    """Log likhna bhi background mein"""
    with open("app.log", "a") as f:
        f.write(f"{message}\n")

@app.post("/register/")
def register_user(
    email: str,
    background_tasks: BackgroundTasks
):
    # User create karo (instantly)
    user = {"email": email, "id": 1}

    # Background mein email bhejo
    background_tasks.add_task(send_email, email, "Welcome!", "Thanks for registering!")

    # Background mein log likho
    background_tasks.add_task(write_log, f"New user registered: {email}")

    # ✅ Turant response — email background mein jaayega
    return {"message": "Registered successfully! Check your email."}
```

> ⚠️ **Common Mistake:** Background tasks sirf simple kaam ke liye hain (email, logging). Heavy processing ke liye **Celery/ARQ** use karo (Chapter 6 mein detail).

---

## 3.3 📁 File Uploads

```python
from fastapi import File, UploadFile

# Single file upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents)
    }

# Multiple files upload
@app.post("/upload-many/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    result = []
    for file in files:
        contents = await file.read()
        result.append({
            "filename": file.filename,
            "size": len(contents)
        })
    return {"files": result}

# File upload with validation
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Type check
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Sirf JPEG, PNG, WebP allowed hai!")

    # Size check (5MB max)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(400, "File 5MB se zyada nahi ho sakti!")

    # Save to disk
    import aiofiles
    file_path = f"uploads/{file.filename}"
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(contents)

    return {"filename": file.filename, "path": file_path}
```

### File + Form Data Together

```python
from fastapi import Form

@app.post("/profile/")
async def create_profile(
    name: str = Form(...),
    bio: str = Form(default=""),
    avatar: UploadFile = File(...)
):
    return {
        "name": name,
        "bio": bio,
        "avatar_filename": avatar.filename
    }
```

> ⚠️ **Common Mistake:** `File` aur `Form` ke saath `Body` (JSON) use nahi kar sakte! Agar JSON + file chahiye toh file alag endpoint pe upload karo.

---

## 3.4 🔌 Middleware

Middleware har request/response ke beech mein run hota hai — logging, timing, auth ke liye.

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    print(f"{request.method} {request.url.path} — {process_time:.4f}s")

    return response
```

### Logging Middleware

```python
import logging

logger = logging.getLogger("api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️  {request.method} {request.url.path}")

    response = await call_next(request)

    logger.info(f"⬅️  {request.method} {request.url.path} → {response.status_code}")
    return response
```

### Custom Middleware Class

```python
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Public routes skip karo
        public_routes = ["/", "/docs", "/health"]
        if request.url.path in public_routes:
            return await call_next(request)

        # Token check
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token missing!"}
            )

        response = await call_next(request)
        return response

app.add_middleware(AuthMiddleware)
```

---

## 3.5 🌐 CORS Setup

**CORS (Cross-Origin Resource Sharing)** — Jab frontend (React) aur backend (FastAPI) alag ports pe ho.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "https://myapp.com",          # Production
    ],
    allow_credentials=True,           # Cookies allow karo
    allow_methods=["*"],              # Sabhi HTTP methods
    allow_headers=["*"],              # Sabhi headers
)
```

> ⚠️ **Common Mistake:** `allow_origins=["*"]` production mein mat use karo! Specific domains likho. `*` sirf development ke liye.

### Development vs Production CORS

```python
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "development":
    origins = ["*"]
else:
    origins = [
        "https://myapp.com",
        "https://www.myapp.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## 3.6 ❌ Exception Handling & Custom Errors

### Built-in HTTPException

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id > 100:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Item lookup failed"}
        )
    return {"item_id": item_id}
```

### Custom Exception Classes

```python
# exceptions.py

class AppException(Exception):
    """Base exception for our app"""
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            status_code=404,
            detail=f"{resource} with id {resource_id} not found",
            error_code="NOT_FOUND"
        )

class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(
            status_code=401,
            detail=detail,
            error_code="UNAUTHORIZED"
        )

class ForbiddenException(AppException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=403,
            detail=detail,
            error_code="FORBIDDEN"
        )
```

### Global Exception Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "path": str(request.url)
            }
        }
    )

# Validation errors ka custom handler
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request data is invalid",
                "details": errors
            }
        }
    )

# Unhandled exceptions handle karo
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Something went wrong! Humari team ko pata chal gaya hai."
            }
        }
    )
```

**Usage:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.find_user(user_id)
    if not user:
        raise NotFoundException("User", user_id)
    return user
```

---

## ⚠️ Common Mistakes

| # | Mistake | Solution |
|---|---------|----------|
| 1 | Depends mein function call karna `Depends(get_db())` | Correct: `Depends(get_db)` — bina brackets! |
| 2 | CORS nahi lagana — frontend se "blocked by CORS" error | CORSMiddleware add karo |
| 3 | Background task mein DB session use karna | Naya session background task ke andar create karo |
| 4 | File upload mein size limit nahi lagana | Content-Type aur size validate karo |
| 5 | Generic exceptions raise karna | Custom exception classes banao — clean error responses |

---

## 💡 Pro Tips

1. **Depends chain** use karo: DB → User → Admin (dependency tree)
2. **`yield`** use karo Depends mein — cleanup automatically ho jaata hai (DB connection close)
3. **Middleware order matters** — pehla middleware sabse pehle chalega
4. **CORS** hamesha sabse pehle add karo — doosre middleware se pehle
5. **Custom exceptions + global handler** = **consistent error format** across API

---

## 🎯 Practice Exercise

1. **Pagination Dependency** banao — `skip`, `limit`, `sort`, `order`
2. **Request timing middleware** likho — response header mein time daalo
3. **Image upload endpoint** banao — type check, size limit (2MB), save to disk
4. **Custom exception handler** — NotFoundException, ValidationError, UnauthorizedException

---

> **Next Chapter:** [04 — Database Integration](./04_database.md) →
