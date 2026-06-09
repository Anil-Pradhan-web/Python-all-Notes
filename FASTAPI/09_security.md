# 📘 Chapter 9: Security — API Keys, HTTPS, Input Validation

> Security compromise karoge toh sab barbaad. Yeh chapter seriously padho.

---

## 9.1 🔑 API Key Authentication (Header-Based)

```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
import os

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

VALID_API_KEYS = {
    os.getenv("API_KEY_1", "key-abc-123"),
    os.getenv("API_KEY_2", "key-xyz-456"),
}

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.get("/api/data")
async def get_data(api_key: str = Depends(verify_api_key)):
    return {"data": "secret stuff", "key_used": api_key[:8] + "..."}
```

### Multiple Auth Methods (API Key OR JWT)

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)
api_key_header_opt = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    api_key: str | None = Security(api_key_header_opt),
):
    if token:
        user = verify_jwt_token(token)
        if user: return user
    if api_key:
        key_info = API_KEY_DB.get(api_key)
        if key_info: return key_info
    raise HTTPException(401, "Provide JWT token or API key")
```

---

## 9.2 🔒 HTTPS / SSL Basics

```bash
# Self-signed cert (dev only)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
# uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

Production mein **Nginx** use karo SSL termination ke liye.

```python
# HTTPS redirect middleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
app.add_middleware(HTTPSRedirectMiddleware)
```

---

## 9.3 🛡️ Input Validation & Sanitization

```python
# ❌ SQL Injection vulnerable
result = db.execute(f"SELECT * FROM users WHERE name = '{name}'")

# ✅ Parameterized (SQLAlchemy automatic)
result = db.query(User).filter(User.name == name).all()

# ✅ XSS prevention
import html

class CommentCreate(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Comment empty nahi ho sakta")
        return v

def render_comment(content: str) -> str:
    # HTML page mein dikhate waqt escape karo
    return html.escape(content)
```

> Rule: Input pe **validate** karo, output/rendering ke waqt **escape** karo. Agar rich text allow karna hai toh `bleach` jaise sanitizer se allowed tags define karo.

---

## 9.4 🔐 Secrets Management

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    openai_api_key: str
    environment: str = "development"

    model_config = {"env_file": ".env", "case_sensitive": False}

settings = Settings()
```

**`.gitignore` mein `.env` zaroor add karo!**

---

## 9.5 Security Headers

```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

---

## 9.6 🔐 Cookie Auth + CSRF

Agar JWT `Authorization: Bearer` header mein bhej rahe ho, CSRF risk usually low hota hai. Agar auth cookie mein token/session store kar rahe ho, CSRF protection zaroor lagao.

Cookie settings:

```python
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,      # HTTPS only
    samesite="lax",   # ya "strict"
    max_age=1800,
)
```

CSRF protection options:

- SameSite cookie use karo
- State-changing requests pe CSRF token require karo
- CORS origins strictly allowlist karo
- `GET` endpoints ko data modify karne ke liye kabhi use mat karo

---

## 9.7 🚦 Rate Limiting Security

Rate limiting detail [Chapter 6](./06_advanced.md) mein hai. Security angle se in endpoints pe strict limits lagao:

- `/auth/login`
- `/auth/register`
- Password reset
- OTP verify
- Expensive AI endpoints
- Public webhooks

---

## ⚠️ Common Mistakes

| Mistake | Solution |
|---------|----------|
| `.env` Git mein push | `.gitignore` mein add karo |
| SQL mein f-strings | Parameterized queries |
| Validation aur escaping confuse karna | Input validate karo, HTML render pe escape karo |
| Error mein stack trace expose | Generic messages in production |
| Cookie auth mein CSRF ignore karna | SameSite + CSRF token use karo |

---

> **Next Chapter:** [10 — Performance Optimization](./10_performance.md) →
