# 📘 Chapter 10: Performance Optimization

> Fast API ko ACTUALLY fast banao — Caching, Pooling, Compression, Async.

---

## 10.1 ⚡ Blocking Calls Audit

Async vs sync ka concept detail mein [Chapter 6](./06_advanced.md) mein cover hai. Performance chapter mein focus yeh hai: **app ko scan kaise karna hai ki kahin event loop block toh nahi ho raha.**

### Audit Checklist

| Check | Risk | Fix |
|-------|------|-----|
| `async def` ke andar `time.sleep()` | Event loop block | `await asyncio.sleep()` |
| `async def` ke andar `requests` | Concurrent requests slow | `httpx.AsyncClient` |
| `async def` ke andar sync SQLAlchemy | DB calls block | sync route `def` ya async SQLAlchemy |
| Large JSON response | Memory + network slow | pagination + GZip |
| CPU-heavy work in request | Worker stuck | queue/Celery/ARQ |

### Quick Scan Commands

```bash
rg "time\.sleep|requests\.|\.all\(" app/
```

Jab bhi `async def` mein sync library dikhe, ya toh async library use karo, ya route ko plain `def` banao so FastAPI threadpool use kare.

---

## 10.2 🗄️ DB Connection Pooling

```python
from sqlalchemy import create_engine

# ✅ Connection pool configured
engine = create_engine(
    "postgresql://user:pass@localhost:5432/mydb",
    pool_size=20,          # Pool mein kitne connections
    max_overflow=10,       # Extra connections (busy time)
    pool_timeout=30,       # Wait time for connection (seconds)
    pool_recycle=1800,     # Connection recycle after 30 min
    pool_pre_ping=True,    # Dead connection check
)
```

### Async Pool

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/mydb",
    pool_size=20,
    max_overflow=10,
    pool_recycle=1800,
)
```

---

## 10.3 🔴 Redis Caching

```bash
pip install redis
```

```python
import redis
import json
from functools import wraps

# Redis client
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Cache decorator
def cache(expire_seconds: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Cache key banao
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Cache mein check karo
            cached = r.get(key)
            if cached:
                return json.loads(cached)

            # Function call karo
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            # Cache mein save karo
            r.setex(key, expire_seconds, json.dumps(result))
            return result
        return wrapper
    return decorator

# Usage
@app.get("/products/")
@cache(expire_seconds=60)  # 1 min cache
async def get_products():
    # Expensive DB query
    products = db.query(Product).all()
    return [p.dict() for p in products]
```

### Manual Cache Control

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    cache_key = f"user:{user_id}"

    # Cache check
    cached = r.get(cache_key)
    if cached:
        return {"data": json.loads(cached), "source": "cache"}

    # DB se fetch
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")

    # Cache mein save (5 min)
    r.setex(cache_key, 300, json.dumps(user.dict()))
    return {"data": user, "source": "database"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, data: UserUpdate):
    # Update DB
    user = crud.update_user(db, user_id, data)

    # ✅ Cache invalidate karo!
    r.delete(f"user:{user_id}")
    return user
```

---

## 10.4 📦 GZip Compression

```python
from fastapi.middleware.gzip import GZipMiddleware

# 500 bytes se zyada responses compress karo
app.add_middleware(GZipMiddleware, minimum_size=500)
```

Response size 50-80% tak kam ho sakta hai! Especially JSON responses ke liye.

---

## 10.5 📊 Quick Optimization Checklist

| Area | Action | Impact |
|------|--------|--------|
| Async | Async DB + httpx use karo | ⭐⭐⭐ |
| DB Pool | `pool_size`, `max_overflow` configure | ⭐⭐⭐ |
| Caching | Redis cache hot data | ⭐⭐⭐ |
| GZip | GZipMiddleware add karo | ⭐⭐ |
| Indexes | DB columns pe indexes lagao | ⭐⭐⭐ |
| Select fields | Sirf required columns fetch karo | ⭐⭐ |
| Pagination | Limit results (max 100) | ⭐⭐ |
| N+1 Queries | `joinedload()` / `selectinload()` use karo | ⭐⭐⭐ |

---

## ⚠️ Common Mistakes

| Mistake | Solution |
|---------|----------|
| Cache invalidate nahi karna | Update/Delete pe cache clear karo |
| Pool size bahut chhota | Traffic ke hisaab se tune karo |
| Async def mein sync calls | `def` use karo ya async library |
| No pagination | Hamesha limit lagao |

---

> **Next Chapter:** [11 — Testing & Deployment](./11_testing_deployment.md) →
