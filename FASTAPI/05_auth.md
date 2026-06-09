# 📘 Chapter 5: Authentication & Authorization — JWT, OAuth2, RBAC

> Security ka chapter — yeh seekhe bina production app nahi bana sakte.

---

## 5.1 🔐 Concepts Samjho Pehle

| Term | Meaning |
|------|---------|
| **Authentication** | "Tu kaun hai?" — Identity verify karna |
| **Authorization** | "Tujhe permission hai?" — Access check karna |
| **JWT** | JSON Web Token — stateless auth token |
| **OAuth2** | Auth protocol — FastAPI built-in support deta hai |
| **RBAC** | Role-Based Access Control — roles ke basis pe permission |

### JWT Token Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.    ← Header (algorithm)
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6...    ← Payload (data)
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQ... ← Signature (verification)
```

---

## 5.2 📦 Dependencies Install

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

| Package | Use |
|---------|-----|
| `python-jose` | JWT token create/verify |
| `passlib[bcrypt]` | Password hashing |
| `python-multipart` | Form data (login form) |

---

## 5.3 🔑 Password Hashing

```python
# app/security.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Plain password → hashed password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check karo password match karta hai ya nahi"""
    return pwd_context.verify(plain_password, hashed_password)

# Usage
hashed = hash_password("mysecretpassword")
print(hashed)  # '$2b$12$EixZaYVK1fsbwRs...'

is_valid = verify_password("mysecretpassword", hashed)
print(is_valid)  # True

is_valid = verify_password("wrongpassword", hashed)
print(is_valid)  # False
```

> ⚠️ **Common Mistake:** Plain text mein password KABHI store mat karo! Hamesha hash karo.

---

## 5.4 🎫 JWT Token Create/Verify

```python
# app/security.py (continued)

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# ⚠️ Yeh values .env file mein honi chahiye — yaha sirf example
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """JWT access token generate karo"""
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict | None:
    """Token verify karo — valid hai toh payload return, nahi toh None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Usage
token = create_access_token({"sub": "anil@example.com", "role": "admin"})
print(token)

payload = verify_token(token)
print(payload)  # {'sub': 'anil@example.com', 'role': 'admin', 'exp': ...}
```

---

## 5.5 🔄 Complete Auth Flow

### Schemas

```python
# app/schemas.py

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None
    role: str = "user"

class UserLogin(BaseModel):
    email: str
    password: str
```

### OAuth2 with Bearer Token

```python
# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.security import verify_token
from app.database import get_db
from app import crud

# Yeh Swagger mein "Authorize" button enable karega
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Token se current user nikaalo"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """Check karo user active hai"""
    if not current_user.is_active:
        raise HTTPException(400, "Inactive user")
    return current_user
```

### Auth Routes

```python
# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check duplicate
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(400, "Email already registered!")

    # crud.create_user ke andar password hash hota hai.
    # Schema object mutate mat karo, warna double-hashing bug aa sakta hai.
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2PasswordRequestForm use karta hai — Swagger mein form dikhega
    - username field = email (OAuth2 standard)
    - password field = password
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(401, "Invalid email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")

    # Token create karo
    access_token = create_access_token(
        data={"sub": user.email, "role": "user"}
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### Protected Routes

```python
# app/routers/users.py

from app.dependencies import get_current_active_user

@router.get("/me", response_model=schemas.UserResponse)
def get_my_profile(current_user = Depends(get_current_active_user)):
    """Apna profile dekho — login required!"""
    return current_user

@router.get("/me/posts", response_model=list[schemas.PostResponse])
def get_my_posts(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_posts(db, current_user.id)
```

---

## 5.6 👑 Role-Based Access Control (RBAC)

```python
# app/dependencies.py

from functools import wraps

class RoleChecker:
    """Reusable role-based dependency"""

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(get_current_active_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{current_user.role}' is not allowed. "
                       f"Required: {self.allowed_roles}"
            )
        return current_user

# Dependencies banao different roles ke liye
allow_admin = RoleChecker(["admin"])
allow_moderator = RoleChecker(["admin", "moderator"])
allow_user = RoleChecker(["admin", "moderator", "user"])
```

### Usage

```python
# Sirf admin
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin = Depends(allow_admin),
    db: Session = Depends(get_db)
):
    crud.delete_user(db, user_id)
    return {"message": "User deleted"}

# Admin + Moderator
@router.put("/posts/{post_id}/approve")
def approve_post(
    post_id: int,
    moderator = Depends(allow_moderator),
    db: Session = Depends(get_db)
):
    crud.approve_post(db, post_id)
    return {"message": "Post approved"}

# Koi bhi logged-in user
@router.post("/posts/")
def create_post(
    post: schemas.PostCreate,
    user = Depends(allow_user),
    db: Session = Depends(get_db)
):
    return crud.create_post(db, post, user.id)
```

---

## 5.7 🔄 Refresh Token Pattern

```python
# Access token — short-lived (15-30 min)
# Refresh token — long-lived (7 days)

REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_refresh_token(data: dict) -> str:
    return create_access_token(
        data=data,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

@router.post("/login", response_model=schemas.TokenPair)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_access_token({"sub": user.email}),
        "refresh_token": create_refresh_token({"sub": user.email}),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    return {
        "access_token": create_access_token({"sub": payload["sub"]}),
        "token_type": "bearer"
    }
```

---

## ⚠️ Common Mistakes

| # | Mistake | Solution |
|---|---------|----------|
| 1 | SECRET_KEY hardcode karna | `.env` file mein rakho, environment variable se padho |
| 2 | Token expiry nahi set karna | Hamesha `exp` claim use karo |
| 3 | Password plain text mein store karna | Hamesha bcrypt hash use karo |
| 4 | Error message mein "email not found" ya "wrong password" alag alag batana | "Invalid email or password" — same message do (security) |
| 5 | Token revocation nahi karna | Blacklist/Redis mein revoked tokens track karo |
| 6 | `python-multipart` install nahi karna | OAuth2PasswordRequestForm ke liye zaruri hai |

---

## 💡 Pro Tips

1. **Access token short-lived rakho** (15-30 min) — kam risk
2. **Refresh token** use karo seamless re-login ke liye
3. **RBAC** ke liye Depends-based RoleChecker pattern best hai
4. **Token mein minimal data** rakho — sirf email/user_id + role
5. **HTTPS** hamesha use karo production mein — token sniffing se bacho
6. **Rate limiting** login endpoint pe lagao — brute force se bacho

---

## 🎯 Practice Exercise

Complete Auth System banao:
1. `/auth/register` — User signup (password hashing)
2. `/auth/login` — JWT token return karo
3. `/auth/me` — Current user profile (protected)
4. RBAC: admin, moderator, user roles
5. Refresh token endpoint

---

> **Next Chapter:** [06 — Advanced FastAPI](./06_advanced.md) →
