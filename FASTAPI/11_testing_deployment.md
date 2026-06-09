# 📘 Chapter 11: Testing & Deployment

> Code likhna 50% kaam hai — test aur deploy karna baaki 50%.

---

## 11.1 🧪 Pytest + TestClient

```bash
pip install pytest httpx
```

### Basic Tests

```python
# tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Laptop", "price": 50000, "category": "electronics"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert "id" in data

def test_create_item_invalid():
    response = client.post(
        "/items/",
        json={"name": "", "price": -100}  # Invalid data
    )
    assert response.status_code == 422  # Validation error

def test_get_item_not_found():
    response = client.get("/items/99999")
    assert response.status_code == 404

def test_get_items_with_pagination():
    response = client.get("/items/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
```

### Test with Auth

```python
def test_protected_endpoint():
    # Login karke token lo
    login_response = client.post(
        "/auth/login",
        data={"username": "test@test.com", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]

    # Protected endpoint call karo
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "email" in response.json()

def test_protected_without_auth():
    response = client.get("/users/me")
    assert response.status_code == 401
```

### Test with DB (Override Dependency)

```python
# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test DB — SQLite in memory
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

```bash
# Tests run karo
pytest -v
pytest -v --tb=short           # Short traceback
pytest tests/test_users.py     # Specific file
pytest -k "test_create"        # Pattern match
pytest --cov=app               # Coverage report
```

---

## 11.2 🐳 Dockerizing FastAPI

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Dependencies install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code copy karo
COPY . .

# Port expose karo
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-Stage Build (Production)

```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Sirf installed packages copy karo
COPY --from=builder /install /usr/local
COPY . .

# Non-root user (security)
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

```bash
# Build & Start
docker-compose up --build

# Background mein run
docker-compose up -d

# Logs dekho
docker-compose logs -f api

# Stop
docker-compose down
```

---

## 11.3 ⚙️ Environment Variables (.env + Pydantic Settings)

```bash
pip install pydantic-settings python-dotenv
```

```python
# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    app_name: str = "My FastAPI App"
    environment: str = "development"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./app.db"

    # Auth
    secret_key: str = "change-this-in-production"
    access_token_expire_minutes: int = 30

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # External APIs
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

# Singleton instance
settings = Settings()
```

```python
# Usage across app
from app.config import settings

if settings.is_production:
    # Production specific behavior
    pass
```

---

## 11.4 🧪 Mocking External Services

Tests mein real OpenAI/payment/email APIs call mat karo. Fast, cheap aur deterministic tests ke liye dependency override ya mock client use karo.

### Dependency Override Pattern

```python
# app/dependencies/ai.py
def get_ai_service():
    return AIService()
```

```python
# app/routers/ai.py
@router.post("/summary")
def summary(
    text: str,
    ai: AIService = Depends(get_ai_service),
):
    return {"summary": ai.summarize(text)}
```

```python
# tests/test_ai.py
class FakeAIService:
    def summarize(self, text: str) -> str:
        return "fake summary"

def test_summary(client):
    app.dependency_overrides[get_ai_service] = lambda: FakeAIService()
    response = client.post("/summary", params={"text": "Long text..."})
    assert response.status_code == 200
    assert response.json()["summary"] == "fake summary"
    app.dependency_overrides.clear()
```

### What to Mock

| Service | Test Strategy |
|---------|---------------|
| LLM APIs | Fake service return fixed text |
| Payment gateway | Fake success/failure responses |
| Email/SMS | Assert function called, don't send |
| Object storage | Local temp folder or fake client |
| Redis queue | In-memory fake or test Redis |

---

## 11.5 🚀 CI/CD Pipeline (GitHub Actions)

Production deploy ka safe flow:

```text
Pull Request
  -> lint
  -> tests
  -> build Docker image
  -> run migrations
  -> deploy app
```

### GitHub Actions Example

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -q
```

---

## ⚠️ Common Mistakes

| Mistake | Solution |
|---------|----------|
| Tests mein production DB use karna | Test DB alag rakho (SQLite/test DB) |
| Docker mein root user chalana | Non-root user create karo |
| `.env` Docker image mein bake karna | `env_file` ya runtime env use karo |
| Tests mein dependencies override nahi karna | `dependency_overrides` use karo |
| `--reload` Docker production mein | Sirf development mein `--reload` |
| Tests mein real external APIs call karna | Fake clients/dependency overrides use karo |

---

## 💡 Pro Tips

1. **`conftest.py`** mein fixtures rakho — reusable across tests
2. **Docker multi-stage** builds = smaller images (100MB vs 500MB+)
3. **`.dockerignore`** file banao — unnecessary files copy mat karo
4. **Health check** Docker mein add karo — container monitoring
5. **`pytest --cov`** — 80%+ coverage aim karo

---

> **Next Chapter:** [12 — Production Practices](./12_production.md) →
