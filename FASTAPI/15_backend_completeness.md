# 📘 Chapter 15: Backend Completeness Checklist

> FastAPI framework seekhna alag cheez hai. Backend engineer banna ka matlab hai API contracts, database discipline, background jobs, observability, deploys, rollback aur failure handling samajhna.

---

## 15.1 Backend Request Lifecycle

Ek production request roughly is flow se guzarti hai:

```text
Client
  -> Load Balancer / Reverse Proxy
  -> FastAPI Middleware
  -> Router
  -> Dependency Injection
  -> Service Layer
  -> Repository / External API / Queue
  -> Response Schema
  -> Logging + Metrics
  -> Client
```

**Rule:** Router thin rakho, service mein business logic, repository mein sirf database access.

```python
@router.post("/orders/", response_model=OrderResponse, status_code=201)
def create_order(
    payload: OrderCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    return service.create_order(payload, user)
```

---

## 15.2 API Contract Design

API contract ka matlab hai frontend/client ko consistently pata ho:

- Request body kaisa hoga
- Response body kaisa hoga
- Error format kaisa hoga
- Pagination/filter/sort ka pattern kya hai
- Breaking changes kaise handle honge

### Resource Naming

```text
GET    /users
POST   /users
GET    /users/{user_id}
PATCH  /users/{user_id}
DELETE /users/{user_id}

GET    /users/{user_id}/posts
POST   /posts/{post_id}/comments
```

**Avoid:**

```text
/getUsers
/createNewUser
/delete-user-now
```

HTTP method already action batata hai, URL resource bataye.

### Consistent Response Envelope

Simple APIs direct model return kar sakti hain. Large apps mein envelope useful hota hai:

```python
from pydantic import BaseModel

class Meta(BaseModel):
    request_id: str | None = None

class ApiResponse(BaseModel):
    success: bool = True
    data: dict | list | None = None
    meta: Meta | None = None
```

Example:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "anil@example.com"
  },
  "meta": {
    "request_id": "2e7f..."
  }
}
```

### Consistent Error Format

```python
class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
```

Example:

```json
{
  "success": false,
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "Email already registered",
    "field": "email"
  }
}
```

---

## 15.3 Pagination, Filtering, Sorting

Har list endpoint mein limit zaroor lagao. Unlimited list endpoint production mein slow bomb hota hai.

### Offset Pagination

```python
from fastapi import Query
from pydantic import BaseModel

class PageMeta(BaseModel):
    total: int
    skip: int
    limit: int

class Page(BaseModel):
    data: list
    meta: PageMeta

def pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return {"skip": skip, "limit": limit}
```

```python
@router.get("/products/")
def list_products(
    page=Depends(pagination_params),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    total = query.count()
    items = query.offset(page["skip"]).limit(page["limit"]).all()
    return {
        "data": items,
        "meta": {"total": total, **page},
    }
```

### Cursor Pagination

Large tables ke liye cursor pagination better hoti hai:

```python
@router.get("/events/")
def list_events(
    after_id: int | None = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Event).order_by(Event.id.asc())
    if after_id:
        query = query.filter(Event.id > after_id)

    rows = query.limit(limit + 1).all()
    has_more = len(rows) > limit
    rows = rows[:limit]

    next_cursor = rows[-1].id if has_more and rows else None
    return {"data": rows, "next_cursor": next_cursor}
```

### Safe Sorting

User input ko directly SQL mein mat daalo. Allowlist use karo:

```python
SORT_FIELDS = {
    "created_at": Product.created_at,
    "price": Product.price,
    "name": Product.name,
}

def apply_sort(query, sort_by: str = "created_at", order: str = "desc"):
    column = SORT_FIELDS.get(sort_by, Product.created_at)
    return query.order_by(column.asc() if order == "asc" else column.desc())
```

---

## 15.4 Database Discipline

Database sirf storage nahi hai, data integrity ka guard bhi hai.

### Constraints Always Add Karo

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
```

**Important constraints:**

- `nullable=False` required fields ke liye
- `unique=True` email/username jaise fields ke liye
- `ForeignKey` relations ke liye
- `index=True` frequently searched fields ke liye
- DB-level constraints business-critical rules ke liye

### Transactions

Multiple writes ek logical operation hain toh transaction mein rakho:

```python
def create_order(db: Session, user_id: int, payload: OrderCreate):
    try:
        order = Order(user_id=user_id, status="pending")
        db.add(order)
        db.flush()  # id mil jaayega, commit abhi nahi

        for item in payload.items:
            db.add(OrderItem(order_id=order.id, product_id=item.product_id, qty=item.qty))

        db.commit()
        db.refresh(order)
        return order
    except Exception:
        db.rollback()
        raise
```

### N+1 Query Problem

Galat:

```python
posts = db.query(Post).all()
for post in posts:
    print(post.author.email)  # Har post ke liye extra query
```

Sahi:

```python
from sqlalchemy.orm import selectinload

posts = (
    db.query(Post)
    .options(selectinload(Post.author))
    .limit(50)
    .all()
)
```

`selectinload()` one-to-many relations mein useful hai. `joinedload()` one-to-one ya many-to-one mein useful hota hai.

### Migration Discipline

```bash
alembic revision --autogenerate -m "add orders table"
alembic upgrade head
alembic downgrade -1
```

Production rules:

- `Base.metadata.create_all()` production mein use mat karo
- Har schema change ka migration banao
- Migration run karne se pehle DB backup/rollback plan rakho
- Data migrations ko carefully test karo

---

## 15.5 Idempotency and Retries

Client retry kare toh duplicate payment/order/email nahi banna chahiye.

### Idempotency Key Pattern

```python
class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    response_json = Column(JSON, nullable=False)
```

```python
@router.post("/payments/")
def create_payment(
    payload: PaymentCreate,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: Session = Depends(get_db),
):
    existing = db.query(IdempotencyRecord).filter_by(key=idempotency_key).first()
    if existing:
        return existing.response_json

    payment = payment_service.charge(payload)
    response = {"payment_id": payment.id, "status": payment.status}

    db.add(IdempotencyRecord(key=idempotency_key, response_json=response))
    db.commit()
    return response
```

Use cases:

- Payments
- Order creation
- Email sending
- Webhook processing

---

## 15.6 The Outbox Pattern (Reliable Background Jobs)

Chapter 6 mein Celery/ARQ queues padhe thay. Par ek critical edge case hota hai: DB write ho gaya, par message queue publish fail ho gaya toh job hamesha ke liye lost ho jaayega. Iske liye **Outbox pattern** use karte hain:

```text
API request -> DB transaction mein business row + outbox row save
Worker -> outbox rows read -> queue/event send -> mark processed
```

```python
class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)
    processed_at = Column(DateTime, nullable=True)
```

```python
def register_user(db: Session, data: UserCreate):
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.flush()

    db.add(OutboxEvent(
        event_type="user.registered",
        payload={"user_id": user.id, "email": user.email},
    ))

    db.commit()
    return user
```

Worker later email send karega. Agar email fail hua toh retry possible hai.

---

## 15.7 File Storage

Local disk dev ke liye okay hai. Production mein object storage use karo:

- S3
- Cloudflare R2
- Google Cloud Storage
- Azure Blob Storage

### Upload Flow

```text
Client -> FastAPI -> validate file -> upload to object storage -> save metadata in DB
```

Metadata table:

```python
class FileAsset(Base):
    __tablename__ = "file_assets"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bucket = Column(String(100), nullable=False)
    object_key = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False)
```

Security checklist:

- Content type validate karo
- File extension trust mat karo
- File size limit rakho
- Random object key use karo
- Private bucket + signed URLs use karo

---

## 15.8 Webhooks

Webhook receiver public endpoint hota hai. Isliye signature verification zaroori hai.

```python
import hmac
import hashlib
from fastapi import Header, Request, HTTPException

WEBHOOK_SECRET = "change-me"

def verify_signature(raw_body: bytes, signature: str) -> bool:
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@router.post("/webhooks/payment")
async def payment_webhook(
    request: Request,
    x_signature: str = Header(...),
    db: Session = Depends(get_db),
):
    raw_body = await request.body()
    if not verify_signature(raw_body, x_signature):
        raise HTTPException(401, "Invalid signature")

    event = await request.json()
    process_payment_event(db, event)
    return {"received": True}
```

Webhook rules:

- Signature verify karo
- Same event duplicate aa sakta hai, idempotent processing rakho
- Jaldi `200 OK` return karo
- Heavy processing queue mein bhejo
- Raw payload store karna debugging mein helpful hota hai

---

## 15.9 External API Clients

External service call ke liye timeout, retry aur error mapping zaroor rakho.

```python
import httpx

class PaymentClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    async def create_payment(self, amount: int) -> dict:
        timeout = httpx.Timeout(10.0, connect=3.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.base_url}/payments",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"amount": amount},
            )
            response.raise_for_status()
            return response.json()
```

Best practices:

- Timeout without fail
- Retry only safe operations
- Secrets settings se lo
- External errors ko clean app errors mein convert karo
- Logs mein API keys/token mask karo

---

## 15.10 Auth Beyond Login

Basic JWT enough nahi hota har app ke liye.

### Access + Refresh Token

- Access token short-lived rakho: 15-30 minutes
- Refresh token long-lived rakho: 7-30 days
- Refresh token DB/Redis mein store karo so revoke possible ho
- Logout pe refresh token revoke karo

### Permission Checks

RBAC simple apps ke liye enough hai:

```python
require_admin = RoleChecker(["admin"])
```

Complex apps mein permission strings better:

```python
class PermissionChecker:
    def __init__(self, required: str):
        self.required = required

    def __call__(self, user=Depends(get_current_user)):
        if self.required not in user.permissions:
            raise HTTPException(403, "Permission denied")
        return user
```

Examples:

```python
can_delete_user = PermissionChecker("users:delete")
can_publish_post = PermissionChecker("posts:publish")
```

---

## 15.11 Feature Flags

Code deploy karna aur feature release karna, dono alag cheezain hain. Feature flag (ya feature toggle) use karke tum runtime pe features enable/disable kar sakte ho bina naya code deploy kiye.

```python
# Simple config-based flag
def check_feature_flag(feature_name: str, db: Session):
    # Ya Redis se read karo
    flag = db.query(FeatureFlag).filter_by(name=feature_name).first()
    return flag.is_active if flag else False

@router.get("/new-algorithm")
def use_new_algo(db: Session = Depends(get_db)):
    if not check_feature_flag("v2_algorithm_enabled", db):
        raise HTTPException(404, "Feature not available")
    return {"message": "Using new algorithm!"}
```
Production apps mein **LaunchDarkly**, **Unleash**, ya **PostHog** use hote hain.

---

## 15.12 API Gateway & Reverse Proxy

Apni FastAPI app ko directly internet pe expose mat karo. Hamesha ek Reverse Proxy (Nginx/Traefik) ya API Gateway (Kong/APISIX) aage rakho.

```text
Client -> API Gateway (SSL, Rate Limit) -> FastAPI (App Logic)
                                        -> Go/NodeJS Service
```

Gateway ke responsibilities:
- **SSL Termination:** HTTPS ko handle karna
- **Global Rate Limiting:** DDOS se bachana
- **Load Balancing:** Multiple Uvicorn/Docker containers mein traffic divide karna
- **Path Routing:** `/api/v1/users` -> FastAPI, `/api/v1/payments` -> Go service

---

## 15.13 Backward Compatibility

API change karte waqt old clients break nahi hone chahiye.

Safe changes:

- Response mein optional field add karna
- New endpoint add karna
- New optional query param add karna

Breaking changes:

- Field rename/remove
- Required field add karna
- Response structure change karna
- Status code behavior change karna

Breaking changes ke liye:

```text
/api/v1/users
/api/v2/users
```

Ya deprecation notice:

```python
@router.get("/old-users", deprecated=True)
def old_users():
    ...
```

---

## 15.14 Production Backend Checklist

Use this before calling a project production-ready:

```text
[ ] API Gateway / Reverse Proxy setup
[ ] Clear project structure
[ ] Pydantic request/response schemas
[ ] Consistent error format
[ ] Auth + authorization checks
[ ] Pagination on list endpoints
[ ] DB indexes and constraints
[ ] Alembic migrations
[ ] Transactions for multi-write operations
[ ] N+1 query prevention
[ ] Rate limiting on auth/sensitive endpoints
[ ] Idempotency for payments/orders/webhooks
[ ] Background queue for slow/critical jobs
[ ] File upload validation + object storage
[ ] Secrets via environment variables
[ ] Structured logs + request id
[ ] Health check + metrics
[ ] Tests with dependency overrides
[ ] Docker image with non-root user
[ ] CI pipeline
[ ] Feature Flags for safe deployments
[ ] Rollback plan
```

---

## 🎯 Practice Exercise

Existing AI Blog API ko production-style backend mein upgrade karo:

1. Posts list endpoint mein pagination + sorting add karo
2. `User.email`, `Post.author_id`, `Post.created_at` pe indexes add karo
3. Alembic migration generate karo
4. Global error response format implement karo
5. Request ID middleware add karo
6. `POST /ai/summarize/{post_id}` ko queue/outbox based banao
7. Webhook receiver add karo with signature verification
8. Docker Compose mein Postgres + Redis add karo
9. Pytest mein auth + post CRUD tests likho
10. GitHub Actions CI add karo

---

> ← [Back to Index](./00_INDEX.md)
