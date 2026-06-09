# 📘 Chapter 14: Mini Project — FastAPI + Auth + DB + LLM API 🚀

> Sab chapters ka combined practical implementation — ek real-world project banana.

---

## 🎯 Project: **AI Blog Platform API**

Features:
- ✅ User Registration & Login (JWT)
- ✅ RBAC (admin, user roles)
- ✅ Blog Posts CRUD
- ✅ AI-powered blog summary generation (LLM)
- ✅ SQLAlchemy + SQLite (swappable to Postgres)
- ✅ Proper project structure
- ✅ Environment config
- ✅ Health check

---

## 📁 Folder Structure

```
ai-blog-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── ai.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── posts.py
│   │   └── ai.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── post_service.py
│   │   └── ai_service.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── security.py
│
├── .env
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 📦 requirements.txt

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
pydantic-settings==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
openai==1.50.0
python-dotenv==1.0.1
```

---

## ⚙️ Step 1: Config & Database

```python
# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "AI Blog API"
    environment: str = "development"
    database_url: str = "sqlite:///./blog.db"
    secret_key: str = "super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openai_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

@lru_cache()
def get_settings():
    return Settings()
```

```python
# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # SQLite only
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 📋 Step 2: Models

```python
# app/models/models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # "user" or "admin"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    ai_summary = Column(Text, nullable=True)  # LLM generated summary
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")
```

---

## 📄 Step 3: Schemas

```python
# app/schemas/user.py

from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=6)

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        if "@" not in v:
            raise ValueError("Valid email do!")
        return v.lower()

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

```python
# app/schemas/post.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class PostCreate(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=10)

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None

class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    ai_summary: str | None
    is_published: bool
    author_id: int
    created_at: datetime
```

```python
# app/schemas/ai.py

from pydantic import BaseModel, Field

class SummarizeRequest(BaseModel):
    text: str = Field(min_length=50, description="Blog content to summarize")

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
```

---

## 🔐 Step 4: Security Utils

```python
# app/utils/security.py

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
```

---

## 🔒 Step 5: Auth Dependencies

```python
# app/dependencies/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.utils.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or inactive")
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin access required")
    return current_user
```

---

## 🛣️ Step 6: Routers

```python
# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already registered")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(400, "Username already taken")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
```

```python
# app/routers/posts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Post, User
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse, status_code=201)
def create_post(
    post: PostCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_post = Post(**post.model_dump(), author_id=user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=list[PostResponse])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.is_published.is_(True))\
        .offset(skip).limit(limit).all()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != user.id and user.role != "admin":
        raise HTTPException(403, "Not your post!")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(post, key, val)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != user.id and user.role != "admin":
        raise HTTPException(403, "Not your post!")
    db.delete(post)
    db.commit()
```

```python
# app/routers/ai.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Post, User
from app.dependencies.auth import get_current_user
from app.services.ai_service import AIService
from app.config import get_settings

router = APIRouter(prefix="/ai", tags=["AI"])
settings = get_settings()

@router.post("/summarize/{post_id}")
def summarize_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Post ka AI summary generate karo aur save karo"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")

    ai = AIService(settings.openai_api_key)
    summary = ai.summarize(post.content)

    # Save summary to DB
    post.ai_summary = summary
    db.commit()

    return {
        "post_id": post_id,
        "summary": summary,
        "original_length": len(post.content),
        "summary_length": len(summary)
    }

@router.post("/generate-ideas")
def generate_ideas(
    topic: str,
    count: int = 5,
    user: User = Depends(get_current_user)
):
    """Blog post ideas generate karo"""
    ai = AIService(settings.openai_api_key)
    ideas = ai.generate_ideas(topic, count)
    return {"topic": topic, "ideas": ideas}
```

---

## 🤖 Step 7: AI Service

```python
# app/services/ai_service.py

from openai import OpenAI

class AIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key) if api_key else None

    def summarize(self, content: str) -> str:
        if not self.client:
            return "AI service not configured (OPENAI_API_KEY missing)"

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the following blog post in 2-3 sentences. Be concise."},
                {"role": "user", "content": content}
            ],
            temperature=0.5,
            max_tokens=200
        )
        return response.choices[0].message.content

    def generate_ideas(self, topic: str, count: int = 5) -> list[str]:
        if not self.client:
            return [f"Sample idea {i+1} for '{topic}'" for i in range(count)]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Generate {count} blog post ideas about the given topic. Return as a numbered list."},
                {"role": "user", "content": topic}
            ],
            temperature=0.8,
            max_tokens=500
        )
        text = response.choices[0].message.content
        return [line.strip() for line in text.split("\n") if line.strip()]
```

---

## 🏠 Step 8: Main App

```python
# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, posts, ai

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    print(f"🚀 {settings.app_name} started! ({settings.environment})")
    yield
    print("🛑 Shutting down...")

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-powered Blog Platform API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(ai.router)

@app.get("/", tags=["Root"])
def root():
    return {"app": settings.app_name, "status": "running"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
```

---

## 🔄 End-to-End Flow

```
1. POST /auth/register   → User signup (password hash + DB save)
2. POST /auth/login       → JWT token receive karo
3. POST /posts/           → Blog post create karo (token required)
4. GET  /posts/           → Sabhi published posts dekho
5. POST /ai/summarize/1   → Post #1 ka AI summary generate karo
6. POST /ai/generate-ideas → New blog ideas generate karo
7. PUT  /posts/1           → Post update karo (owner only)
8. DELETE /posts/1         → Post delete karo (owner/admin only)
```

---

## 🏃 Run Karo

```bash
# .env file banao
cp .env.example .env
# Edit .env with your values

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Browser mein jaao
# http://127.0.0.1:8000/docs   → Swagger UI
# http://127.0.0.1:8000/health → Health check
```

---

## 🐳 Docker (Optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --disabled-password appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t ai-blog-api .
docker run -p 8000:8000 --env-file .env ai-blog-api
```

---

## 🎓 Kya Seekha Is Project Mein?

| Concept | Where Used |
|---------|-----------|
| Path/Query params | Posts listing with pagination |
| Pydantic models | All schemas (validation + serialization) |
| Dependency Injection | `get_db`, `get_current_user`, `require_admin` |
| SQLAlchemy ORM | Models, relationships, CRUD |
| JWT Authentication | Login, protected routes |
| RBAC | Admin-only delete, owner-only update |
| LLM Integration | AI summary, idea generation |
| Project structure | Service layer pattern |
| Config management | pydantic-settings + .env |
| Lifespan events | DB table creation on startup |

---

> **🎉 Congratulations! Ab tum production-level FastAPI developer ho!**
>
> Iske baad kya karo:
> - Alembic migrations add karo
> - Redis caching lagao
> - Pytest tests likho
> - Docker Compose with PostgreSQL banao
> - Frontend (React/Next.js) connect karo

---

> **Next Chapter:** [15 — Backend Completeness Checklist](./15_backend_completeness.md) →
>
> ← [Back to Index](./00_INDEX.md)
