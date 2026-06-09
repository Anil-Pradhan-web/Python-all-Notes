# 📘 Chapter 7: Swagger UI / OpenAPI — Auto Documentation

> FastAPI ki superpower — FREE automatic API documentation. Isko customize karna seekho.

---

## 7.1 🔰 Auto Docs — Out of the Box

FastAPI automatically 2 documentation UIs provide karta hai:

| URL | UI | Use |
|-----|-----|-----|
| `/docs` | Swagger UI | Interactive — API test kar sakte ho |
| `/redoc` | ReDoc | Read-only — clean documentation |

```python
from fastapi import FastAPI

app = FastAPI(
    title="My Awesome API",
    description="Yeh ek production-ready API hai 🚀",
    version="1.0.0",
    contact={
        "name": "Anil Kumar",
        "email": "anil@example.com",
        "url": "https://github.com/anil"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)
```

---

## 7.2 🏷️ Tags — Endpoints Organize Karo

```python
from fastapi import FastAPI

# Tags metadata — Swagger mein sections banata hai
tags_metadata = [
    {
        "name": "Authentication",
        "description": "Login, Register, Token operations",
    },
    {
        "name": "Users",
        "description": "User CRUD operations. **Admin access required** for some endpoints.",
    },
    {
        "name": "Posts",
        "description": "Blog post management",
        "externalDocs": {
            "description": "Detailed docs",
            "url": "https://docs.example.com/posts",
        },
    },
]

app = FastAPI(
    title="Blog API",
    openapi_tags=tags_metadata
)

# Routes pe tags use karo
@app.post("/auth/login", tags=["Authentication"])
def login():
    pass

@app.get("/users/", tags=["Users"])
def get_users():
    pass
```

### APIRouter ke saath Tags

```python
from fastapi import APIRouter

# Router level pe tag — saare endpoints pe apply hoga
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
def get_users():  # Automatically "Users" tag lagega
    pass
```

---

## 7.3 📝 Endpoint Documentation

```python
@app.post(
    "/items/",
    summary="Create a new item",
    description="""
    ## Create Item

    Naya item create karta hai with the following rules:
    - **name** must be unique
    - **price** must be positive
    - Returns the created item with generated ID

    ### Example Usage
    ```json
    {"name": "Laptop", "price": 50000}
    ```
    """,
    response_description="The created item",
    status_code=201,
    tags=["Items"]
)
def create_item(item: Item):
    """
    Yeh endpoint naya item create karta hai.

    - **name**: Item ka naam (unique hona chahiye)
    - **price**: Price in INR (positive number)
    - **category**: Item ki category
    """
    return item
```

> 💡 **Pro Tip:** Docstring (`"""..."""`) bhi Swagger mein description ke taur pe dikhta hai. `description` parameter priority leta hai agar dono diye ho.

---

## 7.4 📋 Response Examples

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., examples=["MacBook Pro"])
    price: float = Field(..., examples=[149999.0])
    category: str = Field(..., examples=["electronics"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "MacBook Pro",
                    "price": 149999.0,
                    "category": "electronics"
                },
                {
                    "name": "Python Book",
                    "price": 599.0,
                    "category": "books"
                }
            ]
        }
    }
```

### Multiple Response Codes Document Karo

```python
from fastapi import HTTPException

@app.get(
    "/items/{item_id}",
    responses={
        200: {
            "description": "Item successfully found",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "Laptop", "price": 50000}
                }
            }
        },
        404: {
            "description": "Item not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Item with id 999 not found"}
                }
            }
        },
        422: {
            "description": "Validation error",
        }
    }
)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(404, f"Item with id {item_id} not found")
    return items_db[item_id]
```

---

## 7.5 🙈 Hide Endpoints

```python
# Endpoint Swagger se hide karo
@app.get("/internal/health", include_in_schema=False)
def internal_health():
    return {"status": "ok"}

# Ya deprecated mark karo
@app.get("/old-endpoint", deprecated=True, tags=["Deprecated"])
def old_endpoint():
    return {"message": "Use /new-endpoint instead"}
```

---

## 7.6 🔧 Custom OpenAPI Schema

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My Custom API",
        version="2.0.0",
        summary="Yeh ek custom OpenAPI schema hai",
        description="""
        ## 🚀 My Production API

        ### Features:
        - User Management
        - Blog Posts
        - Authentication

        ### Authentication
        Use Bearer token in the Authorization header.
        """,
        routes=app.routes,
    )

    # Custom logo add karo
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

---

## 7.7 🔐 Bearer Token Auth in Swagger

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

# Method 1: OAuth2PasswordBearer — Login form + Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# Method 2: HTTPBearer — Sirf Bearer token input
security = HTTPBearer()

@app.get("/secure/")
def secure_route(credentials=Depends(security)):
    return {"token": credentials.credentials}
```

Swagger UI mein ek **"Authorize" 🔒** button dikhega — wahan token paste karke test kar sakte ho!

---

## 7.8 📡 Custom Swagger UI Config

```python
app = FastAPI(
    docs_url="/api/docs",      # Custom docs URL (default: /docs)
    redoc_url="/api/redoc",    # Custom redoc URL (default: /redoc)
    openapi_url="/api/openapi.json",  # OpenAPI JSON URL
)

# Ya completely disable karo (production mein)
app_prod = FastAPI(
    docs_url=None,    # Swagger UI disable
    redoc_url=None,   # ReDoc disable
)
```

### Swagger UI with Custom CSS

```python
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(docs_url=None)  # Default disable karo

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="My API Docs",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="https://example.com/favicon.ico",
    )
```

---

## ⚠️ Common Mistakes

| # | Mistake | Solution |
|---|---------|----------|
| 1 | Docs production mein enable rakhna | `docs_url=None` set karo production mein |
| 2 | Tags nahi use karna | Endpoints organize karo — 50 endpoints bina tags ke chaos |
| 3 | Response examples nahi dena | Frontend devs ko examples chahiye — dedo! |
| 4 | Docstrings nahi likhna | Har endpoint pe description do |
| 5 | Schema mein sensitive info expose karna | `include_in_schema=False` use karo internal endpoints ke liye |

---

## 💡 Pro Tips

1. **Tags metadata** define karo — organized docs FTW
2. **Response examples** do — frontend team khush rahegi
3. **Deprecated endpoints** mark karo — break mat karo, warn karo
4. **OpenAPI JSON export** karo (`/openapi.json`) — Postman mein import kar sakte ho
5. **Internal endpoints** hide karo — security + clean docs

---

> **Next Chapter:** [08 — LLM Integration](./08_llm_integration.md) →
