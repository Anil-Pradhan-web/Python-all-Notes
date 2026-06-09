# 📘 Chapter 6: Advanced FastAPI

> Ab senior engineer wali cheezein — Async, WebSockets, Lifespan, Background Jobs, Rate Limiting, API Versioning.

---

## 6.1 ⚡ async vs sync — Deep Dive

### Kab `async def`, Kab `def`?

```python
# ✅ Use `async def` — jab I/O bound kaam ho (network, DB, file read)
@app.get("/async-endpoint")
async def async_route():
    data = await some_async_db_call()
    return data

# ✅ Use `def` — jab CPU bound kaam ho ya sync library use kar rahe ho
@app.get("/sync-endpoint")
def sync_route():
    data = some_sync_db_call()  # SQLAlchemy sync
    return data
```

### Under the Hood — FastAPI Kaise Handle Karta Hai

```
┌──────────────────────────────────────┐
│         FastAPI (Uvicorn)             │
│                                      │
│  async def → Event Loop mein chalta  │
│  def       → Thread Pool mein chalta │
│                                      │
│  ⚠️ async def + sync code = BLOCK!   │
│  ✅ def + sync code = OK (threadpool) │
└──────────────────────────────────────┘
```

### ⚠️ SABSE BADI MISTAKE

```python
import time

# ❌ GALAT — Event loop BLOCK ho jaayega!
@app.get("/bad")
async def bad_endpoint():
    time.sleep(5)  # Sync sleep in async function — BLOCKS everything!
    return {"message": "Done"}

# ✅ SAHI — async sleep use karo
import asyncio

@app.get("/good-async")
async def good_endpoint():
    await asyncio.sleep(5)  # Non-blocking
    return {"message": "Done"}

# ✅ SAHI — ya plain def use karo (auto threadpool)
@app.get("/good-sync")
def good_sync_endpoint():
    time.sleep(5)  # ThreadPool mein chalega — event loop block nahi hoga
    return {"message": "Done"}
```

### Rule of Thumb

| Situation | Use | Why |
|-----------|-----|-----|
| `await` wali library (httpx, asyncpg) | `async def` | Non-blocking async I/O |
| `requests`, `time.sleep`, sync SQLAlchemy | `def` | FastAPI threadpool mein chalata hai |
| CPU heavy (ML inference, image processing) | `def` + Background Task | Main thread free rakhna |

---

## 6.2 🔌 WebSockets

Real-time communication ke liye — chat apps, live notifications, live data.

### Basic WebSocket

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # Client se message receive karo
            data = await ws.receive_text()
            # Echo back karo
            await ws.send_text(f"Server received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### Chat Room — Multiple Clients

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    """WebSocket connections manage karta hai"""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Sabhi connected clients ko message bhejo"""
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{username}")
async def chat_websocket(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"🟢 {username} joined the chat!")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 {username} left the chat")
```

### WebSocket with Authentication

```python
from fastapi import WebSocket, WebSocketDisconnect, Query
from app.security import verify_token

@app.websocket("/ws/secure")
async def secure_websocket(
    websocket: WebSocket,
    token: str = Query(...)
):
    # Token verify karo
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=4001, reason="Invalid token")
        return

    await websocket.accept()
    user_email = payload["sub"]

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"[{user_email}]: {data}")
    except WebSocketDisconnect:
        print(f"{user_email} disconnected")
```

**Frontend Connection:**
```javascript
const ws = new WebSocket("ws://localhost:8000/ws/secure?token=YOUR_JWT_TOKEN");
ws.onmessage = (event) => console.log(event.data);
ws.send("Hello!");
```

---

## 6.3 🔄 Lifespan Events (Startup/Shutdown)

> Pehle `@app.on_event("startup")` use hota tha — ab **lifespan** recommended hai.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Resources jo app start/stop pe manage karne hain
ml_model = None
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    yield se pehle = STARTUP
    yield ke baad = SHUTDOWN
    """
    # ✅ STARTUP — resources initialize karo
    global ml_model, db_pool
    print("🚀 Starting up...")

    ml_model = load_ml_model()
    db_pool = await create_db_pool()

    yield  # ← App yahan run karta hai

    # ✅ SHUTDOWN — cleanup karo
    print("🛑 Shutting down...")
    await db_pool.close()
    ml_model = None

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
def predict(text: str):
    return {"prediction": ml_model.predict(text)}
```

### Real-World: Redis + DB Pool

```python
import redis.asyncio as redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
    app.state.db_pool = await create_async_engine(DATABASE_URL)
    print("✅ Redis & DB connected")

    yield

    # Shutdown
    await app.state.redis.close()
    await app.state.db_pool.dispose()
    print("🛑 Connections closed")

app = FastAPI(lifespan=lifespan)

@app.get("/cached-data")
async def get_cached(request: Request):
    redis_client = request.app.state.redis
    cached = await redis_client.get("my_key")
    if cached:
        return {"data": cached, "source": "cache"}
    return {"data": "fresh", "source": "db"}
```

---

## 6.4 📋 Background Jobs (Celery / ARQ)

### Option 1: Celery (Popular, Battle-tested)

```bash
pip install celery[redis]
```

```python
# app/celery_worker.py

from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery_app.conf.task_track_started = True

@celery_app.task
def send_email_task(email: str, subject: str, body: str):
    """Heavy email task — Celery worker mein chalega"""
    import time
    time.sleep(10)  # Simulate heavy work
    print(f"Email sent to {email}")
    return {"status": "sent", "email": email}

@celery_app.task
def generate_report_task(user_id: int):
    """Report generation — time consuming"""
    import time
    time.sleep(30)
    return {"status": "completed", "user_id": user_id}
```

```python
# FastAPI route mein use karo
from app.celery_worker import send_email_task, generate_report_task

@app.post("/send-email/")
def send_email(email: str, subject: str, body: str):
    task = send_email_task.delay(email, subject, body)
    return {"task_id": task.id, "status": "queued"}

@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }
```

```bash
# Celery worker start karo
celery -A app.celery_worker worker --loglevel=info
```

### Option 2: ARQ (Async, Lightweight)

```bash
pip install arq
```

```python
# app/worker.py

from arq import create_pool
from arq.connections import RedisSettings

async def send_notification(ctx, user_id: int, message: str):
    """Async background task"""
    print(f"Sending notification to user {user_id}: {message}")
    await asyncio.sleep(2)
    return {"sent": True}

class WorkerSettings:
    functions = [send_notification]
    redis_settings = RedisSettings(host="localhost", port=6379)
```

```python
# FastAPI mein use karo
from arq import create_pool
from arq.connections import RedisSettings

@app.post("/notify/")
async def notify(user_id: int, message: str):
    redis = await create_pool(RedisSettings())
    job = await redis.enqueue_job("send_notification", user_id, message)
    return {"job_id": job.job_id}
```

---

## 6.5 🚦 Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 10 requests per minute
@app.get("/api/data")
@limiter.limit("10/minute")
async def get_data(request: Request):
    return {"data": "here"}

# Login pe strict limit
@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request):
    return {"token": "..."}

# Different limits for different users
@app.get("/api/premium")
@limiter.limit("100/minute")  # Premium users ke liye zyada
async def premium_data(request: Request):
    return {"data": "premium"}
```

---

## 6.6 📌 API Versioning

### Method 1: URL-based (Recommended)

```python
from fastapi import APIRouter, FastAPI

app = FastAPI()

# V1 Router
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/users/")
def get_users_v1():
    return {"version": 1, "users": ["format_old"]}

# V2 Router — improved response
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users/")
def get_users_v2():
    return {
        "version": 2,
        "data": {"users": ["format_new"]},
        "meta": {"total": 1, "page": 1}
    }

app.include_router(v1_router)
app.include_router(v2_router)
```

### Method 2: Header-based

```python
from fastapi import Header

@app.get("/api/users/")
def get_users(api_version: str = Header(default="v1", alias="X-API-Version")):
    if api_version == "v2":
        return {"version": 2, "data": {"users": []}}
    return {"version": 1, "users": []}
```

### Best Practice: Folder Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── users.py
│   │   │   └── posts.py
│   │   └── schemas.py
│   ├── v2/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── users.py     # Updated response format
│   │   │   └── posts.py
│   │   └── schemas.py
│   └── router.py
```

---

## ⚠️ Common Mistakes

| # | Mistake | Solution |
|---|---------|----------|
| 1 | `async def` mein sync code (requests, time.sleep) | `def` use karo ya asyncio version use karo |
| 2 | WebSocket mein auth nahi lagana | Query param se token verify karo |
| 3 | `on_event("startup")` use karna | `lifespan` context manager use karo (modern way) |
| 4 | BackgroundTasks ko Celery ki jagah heavy kaam ke liye use karna | Simple tasks = BackgroundTasks, Heavy = Celery/ARQ |
| 5 | API versioning nahi karna | Start se v1 prefix use karo |

---

## 💡 Pro Tips

1. **`httpx.AsyncClient`** use karo `requests` ki jagah async endpoints mein
2. **WebSocket heartbeat** implement karo — dead connections detect karne ke liye
3. **Lifespan** mein startup checks daalo — DB connectivity, Redis, etc.
4. **Rate limiting** login, register, aur expensive endpoints pe zaroor lagao
5. **API versioning** shuru se karo — baad mein breaking changes handle karna mushkil hai

---

> **Next Chapter:** [07 — Swagger / OpenAPI](./07_swagger_openapi.md) →
