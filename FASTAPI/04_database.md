# 📘 Chapter 4: Database Integration — SQLAlchemy + FastAPI

> Ab asli backend engineer wali baat — Database CRUD, Migrations, aur Async DB.

---

## 4.1 🏗️ SQLAlchemy Setup

```bash
pip install sqlalchemy alembic psycopg2-binary
# ya SQLite ke liye kuch aur install nahi karna (built-in hai)
```

### Database Configuration

```python
# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite (development ke liye)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# PostgreSQL (production ke liye)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite ke liye zaruri
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ DB Dependency — har request pe fresh session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 4.2 📋 Models Define Karo

```python
# app/models.py

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship
    author = relationship("User", back_populates="posts")
```

---

## 4.3 📄 Pydantic Schemas (Request/Response)

```python
# app/schemas.py

from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime

# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_published: bool
    created_at: datetime
    author_id: int

class PostWithAuthor(PostResponse):
    """Post with nested author info"""
    author: UserResponse
```

> 💡 **Pro Tip:** `model_config = ConfigDict(from_attributes=True)` zaruri hai SQLAlchemy objects ko Pydantic models mein convert karne ke liye.

---

## 4.4 🔧 CRUD Operations

```python
# app/crud.py

from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password

# --- User CRUD ---

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    # Password hashing detail Chapter 5 mein hai
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # DB se fresh data le aao (id, created_at, etc.)
    return db_user

def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


# --- Post CRUD ---

def create_post(db: Session, post: schemas.PostCreate, author_id: int) -> models.Post:
    db_post = models.Post(**post.model_dump(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10) -> list[models.Post]:
    return db.query(models.Post)\
        .filter(models.Post.is_published.is_(True))\
        .offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int) -> models.Post | None:
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate) -> models.Post | None:
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None

    # Sirf wo fields update karo jo bheje gaye hain
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int) -> bool:
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return False
    db.delete(db_post)
    db.commit()
    return True
```

---

## 4.5 🌐 API Routes

```python
# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(400, "Email already registered!")
    return crud.create_user(db, user)

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

```python
# app/routers/posts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=schemas.PostResponse, status_code=201)
def create_post(
    post: schemas.PostCreate,
    author_id: int,  # Baad mein auth se aayega
    db: Session = Depends(get_db)
):
    return crud.create_post(db, post, author_id)

@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)

@router.get("/{post_id}", response_model=schemas.PostWithAuthor)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    db: Session = Depends(get_db)
):
    post = crud.update_post(db, post_id, post_update)
    if not post:
        raise HTTPException(404, "Post not found")
    return post

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    if not crud.delete_post(db, post_id):
        raise HTTPException(404, "Post not found")
```

### Main App mein Routers Include Karo

```python
# main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, posts

# Tables create karo (development ke liye)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
def root():
    return {"message": "Blog API is running!"}
```

---

## 4.6 🔄 Alembic Migrations

> Production mein `Base.metadata.create_all()` mat use karo! Alembic use karo — yeh database ka Git hai.

```bash
# Setup
pip install alembic
alembic init alembic
```

### `alembic/env.py` Configure Karo

```python
# alembic/env.py — key changes

from app.database import Base
from app.models import User, Post  # Import all models!

target_metadata = Base.metadata
```

### `alembic.ini` mein Database URL

```ini
# alembic.ini
sqlalchemy.url = sqlite:///./app.db
```

### Migration Commands

```bash
# Naya migration banao (auto detect changes)
alembic revision --autogenerate -m "create users and posts tables"

# Migration run karo
alembic upgrade head

# Ek step peeche jaao
alembic downgrade -1

# Current version dekho
alembic current

# History dekho
alembic history
```

### Example Migration File

```python
# alembic/versions/xxxx_create_users_and_posts.py
# Yeh alembic automatically generate karta hai!

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )

def downgrade():
    op.drop_table('users')
```

> 💡 **Pro Tip:** Har database schema change ke liye naya migration banao. Production mein directly table modify mat karo!

---

## 4.7 ⚡ Async Database (Advanced)

```bash
pip install sqlalchemy[asyncio] aiosqlite  # SQLite async
# ya
pip install sqlalchemy[asyncio] asyncpg    # PostgreSQL async
```

```python
# app/database_async.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./app.db"
# PostgreSQL: "postgresql+asyncpg://user:pass@localhost:5432/mydb"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Async CRUD

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

### Async Routes

```python
@router.get("/users/", response_model=list[schemas.UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_users(db, skip, limit)
```

---

## 4.8 🧱 Production DB Notes

### Indexes & Constraints

ORM validation enough nahi hoti. Database level pe bhi rules lagao:

```python
email = Column(String(100), unique=True, index=True, nullable=False)
author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
created_at = Column(DateTime, default=datetime.utcnow, index=True)
```

### Transactions for Multi-Step Writes

```python
def publish_post(db: Session, post_id: int, user_id: int):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if not post:
            raise HTTPException(404, "Post not found")

        post.is_published = True
        db.add(models.AuditLog(user_id=user_id, action="post.published", target_id=post_id))

        db.commit()
        db.refresh(post)
        return post
    except Exception:
        db.rollback()
        raise
```

### N+1 Queries Avoid Karo

```python
from sqlalchemy.orm import selectinload

posts = (
    db.query(models.Post)
    .options(selectinload(models.Post.author))
    .offset(skip)
    .limit(limit)
    .all()
)
```

> Detail checklist: [Chapter 15 — Backend Completeness](./15_backend_completeness.md)

---

## ⚠️ Common Mistakes

| # | Mistake | Solution |
|---|---------|----------|
| 1 | DB session close nahi karna | `get_db()` mein `yield` + `finally: db.close()` |
| 2 | `Base.metadata.create_all()` production mein use karna | Alembic migrations use karo |
| 3 | Models import nahi karna Alembic mein | `env.py` mein sabhi models import karo |
| 4 | `commit()` bhool jaana | Create/Update/Delete ke baad `db.commit()` zaroori |
| 5 | Relationship lazy loading async mein | `selectinload()` ya `joinedload()` use karo |
| 6 | Multi-step write mein rollback nahi lagana | `try/except` + `db.rollback()` use karo |

---

## 🎯 Practice Exercise

**Blog API banao:**
1. Users + Posts tables (SQLAlchemy models)
2. Pydantic schemas (Create, Update, Response)
3. Full CRUD operations
4. Alembic migration setup
5. Relationships: User → Posts (one to many)

**Bonus:** Async version banao with `asyncpg`

---

> **Next Chapter:** [05 — Authentication & Authorization](./05_auth.md) →
