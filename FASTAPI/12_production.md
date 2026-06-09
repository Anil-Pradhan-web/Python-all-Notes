# 📘 Chapter 12: Production-Grade Practices 🚀

> Ab app ko production-ready banao — Uvicorn, Logging, Health Checks, Metrics.

---

## 12.1 🖥️ Uvicorn + Gunicorn Setup

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Gunicorn with Uvicorn workers (Linux/Docker)
pip install gunicorn

gunicorn app.main:app \
    -w 4 \                          # Workers = (2 * CPU cores) + 1
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

### Docker CMD

```dockerfile
CMD ["gunicorn", "app.main:app", \
     "-w", "4", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-b", "0.0.0.0:8000", \
     "--timeout", "120"]
```

> 💡 **Workers formula:** `(2 × CPU cores) + 1`. 4 core machine = 9 workers.

---

## 12.2 ❤️ Health Check Endpoints

```python
from fastapi import APIRouter
from datetime import datetime
import psutil

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    """Basic health check — load balancer ke liye"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@router.get("/health/detailed")
def detailed_health():
    """Detailed health with system info"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
        },
        "checks": {
            "database": check_db_connection(),
            "redis": check_redis_connection(),
        }
    }

def check_db_connection() -> dict:
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def check_redis_connection() -> dict:
    try:
        r.ping()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
```

---

## 12.3 📝 Logging (Loguru)

```bash
pip install loguru
```

```python
# app/logger.py

from loguru import logger
import sys

# Console logging
logger.remove()  # Default handler hatao
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
    level="INFO"
)

# File logging with rotation
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="100 MB",    # Naya file 100MB pe
    retention="30 days",  # 30 din purane delete
    compression="zip",    # Compress karo
    level="DEBUG"
)

# JSON logging (production — log aggregation ke liye)
logger.add(
    "logs/app.json",
    serialize=True,  # JSON format
    rotation="50 MB"
)
```

### Logging Middleware

```python
from app.logger import logger

@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start = time.time()

    # Request log
    logger.info(f"➡️  {request.method} {request.url.path}")

    response = await call_next(request)

    # Response log
    duration = round(time.time() - start, 4)
    logger.info(
        f"⬅️  {request.method} {request.url.path} "
        f"→ {response.status_code} ({duration}s)"
    )
    return response
```

### Usage

```python
from app.logger import logger

@app.post("/users/")
def create_user(user: UserCreate):
    logger.info(f"Creating user: {user.email}")
    try:
        db_user = crud.create_user(db, user)
        logger.success(f"User created: {db_user.id}")
        return db_user
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise
```

---

## 12.4 🔍 Request ID Tracing

Har request ko unique ID do — distributed systems mein debugging ke liye.

```python
import uuid
from fastapi import Request

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    # Request state mein store karo
    request.state.request_id = request_id

    logger.bind(request_id=request_id).info(
        f"{request.method} {request.url.path}"
    )

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

---

## 12.5 📊 Prometheus Metrics

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# One line setup!
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
```

Ab `/metrics` pe jaao — Prometheus format mein metrics milenge:
- Request count
- Response time
- Error rates
- Active requests

### Custom Metrics

```python
from prometheus_client import Counter, Histogram

# Custom counters
user_signups = Counter("user_signups_total", "Total user signups")
api_calls = Counter("api_calls_total", "Total API calls", ["method", "endpoint"])
response_time = Histogram("response_time_seconds", "Response time")

@app.post("/auth/register")
def register(user: UserCreate):
    user_signups.inc()  # Counter increment
    api_calls.labels(method="POST", endpoint="/auth/register").inc()
    # ... create user
```

---

## 12.6 🐞 Sentry Integration (Error Tracking)

Production mein "server down hai" enough information nahi hoti. Errors automatically track hone chahiye.

```bash
pip install sentry-sdk[fastapi]
```

```python
import sentry_sdk
from fastapi import FastAPI

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    environment=settings.environment,
    traces_sample_rate=0.1,
)

app = FastAPI()
```

---

## 12.7 🚀 Deployment Runbook

Production deploy random commands ka set nahi hona chahiye. Ek repeatable runbook rakho.

```text
1. Build Docker image
2. Run tests
3. Push image to registry
4. Run DB migrations
5. Deploy new app version
6. Hit /health
7. Check logs + metrics
8. Rollback if error rate spike hota hai
```

### Migration Safety

Backward-compatible migrations pehle run karo:

```text
Deploy 1: add nullable column
Deploy 2: app starts writing new column
Deploy 3: backfill old rows
Deploy 4: make column non-null if needed
```

### Rollback Plan

Har deploy ke pehle ye clear hona chahiye:

- Previous image tag kya hai?
- DB migration reversible hai ya nahi?
- Feature flag off kar sakte hain kya?
- Error threshold kya hai rollback ke liye?

> Deep checklist: [Chapter 15 — Backend Completeness](./15_backend_completeness.md)

---

## 🏗️ Production Deployment Checklist

```
✅ Gunicorn + Uvicorn workers configured
✅ Health check endpoints (/health)
✅ Structured logging (loguru/JSON)
✅ Request ID tracing
✅ Prometheus metrics
✅ HTTPS enabled (Nginx + Let's Encrypt)
✅ CORS properly configured
✅ Rate limiting on sensitive endpoints
✅ Environment variables (no hardcoded secrets)
✅ Docker + docker-compose
✅ Error handling (custom exception handlers)
✅ Database connection pooling
✅ Swagger docs disabled in production
✅ Rollback plan documented
```

---

> **Next Chapter:** [13 — Project Structure](./13_project_structure.md) →
