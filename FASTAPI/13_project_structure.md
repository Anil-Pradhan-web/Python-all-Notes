# 📘 Chapter 13: Project Structure — Scalable Architecture 🏗️

> Yeh chapter SABSE IMPORTANT hai. Sahi structure ke bina bada project maintain karna impossible hai.

---

## 13.1 ❌ Galat Structure (Beginners Ki Mistake)

```
# ❌ Sab kuch ek file mein — "main.py of doom"
project/
├── main.py          # 2000+ lines — routes, models, schemas, logic SAB
├── requirements.txt
└── .env
```

> Yeh chalta hai 5 endpoints tak. 50 endpoints pe nightmare ban jaata hai.

---

## 13.2 ✅ Production-Grade Structure

```
project/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance + lifespan
│   ├── config.py               # Settings (pydantic-settings)
│   ├── database.py             # DB engine, session, get_db
│   │
│   ├── models/                 # SQLAlchemy models (DB tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── base.py             # Base = declarative_base()
│   │
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py             # UserCreate, UserUpdate, UserResponse
│   │   ├── post.py
│   │   └── common.py           # PaginationParams, SuccessResponse
│   │
│   ├── routers/                # API route definitions
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── ai.py
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── post_service.py
│   │   ├── auth_service.py
│   │   └── llm_service.py
│   │
│   ├── repositories/           # Database access layer (CRUD)
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── post_repo.py
│   │
│   ├── dependencies/           # Depends() functions
│   │   ├── __init__.py
│   │   ├── auth.py             # get_current_user, RoleChecker
│   │   ├── database.py         # get_db
│   │   └── pagination.py       # common_pagination
│   │
│   ├── middleware/             # Custom middleware
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── cors.py
│   │   └── request_id.py
│   │
│   ├── exceptions/            # Custom exceptions + handlers
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── handlers.py
│   │
│   └── utils/                 # Helper functions
│       ├── __init__.py
│       ├── security.py        # hash_password, verify_password, JWT
│       └── helpers.py
│
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                     # Test files
│   ├── __init__.py
│   ├── conftest.py            # Fixtures
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_posts.py
│
├── logs/                      # Log files (gitignored)
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env                       # Environment variables (gitignored)
├── .env.example               # Example env (committed)
├── .gitignore
└── README.md
```

---

## 13.3 🔄 Service Layer Pattern (Route → Service → Repository)

Yeh production apps ka **CORE PATTERN** hai. 3 layers mein kaam divide karo:

```
┌─────────────────────────────────────────────────┐
│  CLIENT (Frontend / Mobile / Postman)            │
└──────────────────────┬──────────────────────────┘
                       │ HTTP Request
                       ▼
┌─────────────────────────────────────────────────┐
│  ROUTER (routers/users.py)                       │
│  → Request receive karo                          │
│  → Input validate karo (Pydantic)                │
│  → Service function call karo                    │
│  → Response return karo                          │
└──────────────────────┬──────────────────────────┘
                       │ Function Call
                       ▼
┌─────────────────────────────────────────────────┐
│  SERVICE (services/user_service.py)              │
│  → Business logic execute karo                   │
│  → Multiple repos combine karo                   │
│  → Validation / Authorization checks             │
│  → External API calls                            │
└──────────────────────┬──────────────────────────┘
                       │ DB Operations
                       ▼
┌─────────────────────────────────────────────────┐
│  REPOSITORY (repositories/user_repo.py)          │
│  → Database CRUD operations                      │
│  → SQL queries                                   │
│  → Data access only — NO business logic          │
└─────────────────────────────────────────────────┘
```

### Layer 1: Router (Thin — sirf routing)

```python
# app/routers/users.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.common import PaginationParams
from app.services.user_service import UserService
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Router sirf receive aur return karta hai — logic service mein hai"""
    service = UserService(db)
    return service.create_user(user_data)

@router.get("/", response_model=list[UserResponse])
def get_users(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.get_users(pagination.skip, pagination.limit)

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user=Depends(get_current_active_user)):
    return current_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.update_user(user_id, user_data, current_user)
```

### Layer 2: Service (Business Logic)

```python
# app/services/user_service.py

from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password
from app.exceptions.base import (
    NotFoundException, ConflictException, ForbiddenException
)

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, user_data: UserCreate):
        # Business rule: duplicate email check
        existing = self.repo.get_by_email(user_data.email)
        if existing:
            raise ConflictException("User", "email", user_data.email)

        # Business rule: password hash karo
        hashed_pw = hash_password(user_data.password)

        return self.repo.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pw
        )

    def get_users(self, skip: int = 0, limit: int = 10):
        return self.repo.get_all(skip=skip, limit=limit)

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        return user

    def update_user(self, user_id: int, user_data: UserUpdate, current_user):
        # Business rule: sirf apna profile ya admin update kar sakta hai
        if current_user.id != user_id and current_user.role != "admin":
            raise ForbiddenException("You can only update your own profile")

        user = self.get_user(user_id)
        return self.repo.update(user, user_data.model_dump(exclude_unset=True))
```

### Layer 3: Repository (Database Access Only)

```python
# app/repositories/user_repo.py

from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def update(self, user: User, update_data: dict) -> User:
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> bool:
        self.db.delete(user)
        self.db.commit()
        return True
```

---

## 13.4 ⚙️ Config Management

```python
# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "FastAPI App"
    environment: str = "development"
    debug: bool = False
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "sqlite:///./app.db"
    db_pool_size: int = 20
    db_max_overflow: int = 10

    # Auth
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # External
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

@lru_cache()
def get_settings() -> Settings:
    """Cached settings — .env sirf ek baar read hoga"""
    return Settings()
```

### `.env.example` — Team ke liye template

```bash
# .env.example (Git mein commit karo)

# App
APP_NAME=FastAPI App
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Auth
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379/0

# External APIs
OPENAI_API_KEY=sk-your-key-here
```

---

## 13.5 🧩 Main App Assembly

```python
# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import get_settings
from app.routers import auth, users, posts, ai
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.exceptions.handlers import register_exception_handlers

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 Starting {settings.app_name} ({settings.environment})")
    yield
    # Shutdown
    print("🛑 Shutting down...")

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# --- Middleware (order matters!) ---
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not settings.is_production else ["https://myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception Handlers ---
register_exception_handlers(app)

# --- Routers ---
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(posts.router, prefix=settings.api_prefix)
app.include_router(ai.router, prefix=settings.api_prefix)

# --- Health Check ---
@app.get("/health")
def health():
    return {"status": "healthy", "environment": settings.environment}
```

---

## 13.6 📋 Common Schemas

```python
# app/schemas/common.py

from pydantic import BaseModel, Field
from fastapi import Query

class PaginationParams:
    """Reusable pagination dependency"""
    def __init__(
        self,
        skip: int = Query(default=0, ge=0, description="Records to skip"),
        limit: int = Query(default=10, ge=1, le=100, description="Max records"),
    ):
        self.skip = skip
        self.limit = limit

class SuccessResponse(BaseModel):
    success: bool = True
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: dict = Field(
        example={"code": "NOT_FOUND", "message": "Resource not found"}
    )
```

---

## 13.7 🛡️ Custom Exceptions

```python
# app/exceptions/base.py

class AppException(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str = "ERROR"):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id):
        super().__init__(404, f"{resource} with id {resource_id} not found", "NOT_FOUND")

class ConflictException(AppException):
    def __init__(self, resource: str, field: str, value: str):
        super().__init__(409, f"{resource} with {field} '{value}' already exists", "CONFLICT")

class ForbiddenException(AppException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(403, detail, "FORBIDDEN")

class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(401, detail, "UNAUTHORIZED")
```

```python
# app/exceptions/handlers.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions.base import AppException

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {"code": exc.error_code, "message": exc.detail}
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        errors = [
            {"field": ".".join(str(l) for l in e["loc"]), "message": e["msg"]}
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {"code": "VALIDATION_ERROR", "details": errors}
            }
        )
```

---

## ⚠️ Common Mistakes

| Mistake | Solution |
|---------|----------|
| Business logic router mein likhna | Service layer mein rakho |
| Repository mein authorization check | Service layer mein karo |
| Settings har jagah import karna | Dependency injection use karo |
| Ek file mein sab models | Alag files: user.py, post.py |
| `__init__.py` nahi banana | Har directory mein zaroori hai |

---

## 💡 Pro Tips

1. **Router thin rakho** — sirf receive + return, logic nahi
2. **Service = Brain** — sab business logic yahan
3. **Repository = Database only** — SQL queries, no logic
4. **Config ek jagah** — pydantic-settings + .env
5. **Exceptions organized** — custom classes + global handlers
6. **`@lru_cache`** settings pe — .env baar baar load nahi hogi

---

> **Next Chapter:** [14 — Mini Project](./14_mini_project.md) →
