# 📘 Chapter 2: Pydantic — Data Validation Ka Raja 👑

> FastAPI ki asli taaqat Pydantic se aati hai. Yeh chapter samajh liya toh validation, serialization sab clear ho jaayega.

---

## 2.1 🔰 BaseModel — Foundation

Pydantic ka `BaseModel` ek **data class on steroids** hai. Yeh automatically:
- ✅ Data validate karta hai
- ✅ Type conversion karta hai
- ✅ Error messages deta hai
- ✅ JSON serialization/deserialization karta hai

```python
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True  # default value
    created_at: datetime = datetime.now()

# ✅ Valid data
user = User(name="Anil", age=21, email="anil@example.com")
print(user.model_dump())
# {'name': 'Anil', 'age': 21, 'email': 'anil@example.com', 'is_active': True, 'created_at': ...}

# ✅ Type coercion — "22" → 22 (str se int)
user2 = User(name="Rahul", age="22", email="rahul@test.com")
print(user2.age)  # 22 (int)

# ❌ Invalid data — error milega
try:
    user3 = User(name="Test", age="not_a_number", email="test@test.com")
except Exception as e:
    print(e)
    # validation error for User
    # age: Input should be a valid integer
```

### Pydantic v2 Important Methods

```python
user = User(name="Anil", age=21, email="anil@example.com")

# Dict mein convert karo
user.model_dump()             # → dict
user.model_dump(exclude={"created_at"})  # kuch fields hatao
user.model_dump(include={"name", "email"})  # sirf specific fields

# JSON mein convert karo
user.model_dump_json()        # → JSON string

# Schema dekho
User.model_json_schema()      # → JSON Schema (OpenAPI ke liye)
```

> ⚠️ **Common Mistake:** Purane tutorials mein `.dict()` aur `.json()` dikhega — woh Pydantic v1 hai. Pydantic v2 mein `.model_dump()` aur `.model_dump_json()` use karo.

---

## 2.2 🔒 Field Validation

`Field()` use karke har field pe constraints laga sakte ho.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(
        ...,                    # ... means required
        min_length=2,
        max_length=100,
        title="Product Name",
        description="Product ka naam"
    )
    price: float = Field(
        ...,
        gt=0,        # greater than 0
        le=1000000,  # less than or equal to 10 lakh
        description="Price in INR"
    )
    quantity: int = Field(
        default=0,
        ge=0,    # greater than or equal to 0
        le=10000
    )
    category: str = Field(
        ...,
        pattern="^[a-zA-Z_]+$",  # regex pattern
        examples=["electronics", "clothing"]
    )
```

### Field Constraints Cheat Sheet

| Constraint | Type | Meaning |
|-----------|------|---------|
| `gt` | number | Greater than |
| `ge` | number | Greater than or equal |
| `lt` | number | Less than |
| `le` | number | Less than or equal |
| `min_length` | string | Minimum length |
| `max_length` | string | Maximum length |
| `pattern` | string | Regex pattern |
| `multiple_of` | number | Multiple of given number |
| `...` (Ellipsis) | any | Required field (no default) |

---

## 2.3 ❓ Optional Fields & Default Values

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogPost(BaseModel):
    title: str                                # Required
    content: str                              # Required
    summary: str | None = None                # Optional (Python 3.10+)
    tags: list[str] = []                      # Default empty list
    is_published: bool = False                # Default False
    published_at: datetime | None = None      # Optional datetime
    views: int = 0                            # Default 0

# Sirf required fields dena zaroori hai
post = BlogPost(title="FastAPI Guide", content="Bahut badiya framework hai...")
print(post.model_dump())
# {
#   'title': 'FastAPI Guide',
#   'content': 'Bahut badiya framework hai...',
#   'summary': None,
#   'tags': [],
#   'is_published': False,
#   'published_at': None,
#   'views': 0
# }
```

> 💡 **Pro Tip:** `str | None = None` aur `Optional[str] = None` dono same hain. Python 3.10+ mein `|` syntax use karo — zyada clean hai.

---

## 2.4 🏗️ Nested Models

Real-world mein data nested hota hai — Pydantic isme expert hai.

```python
from pydantic import BaseModel, EmailStr

# pip install pydantic[email]  ← EmailStr ke liye

class Address(BaseModel):
    street: str
    city: str
    state: str
    pin_code: str = Field(pattern=r"^\d{6}$")  # 6 digit pin

class SocialLinks(BaseModel):
    github: str | None = None
    linkedin: str | None = None
    twitter: str | None = None

class UserProfile(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(ge=13, le=120)
    address: Address                          # Nested model
    social: SocialLinks | None = None         # Optional nested
    skills: list[str] = []                    # List of strings
    education: list[dict] = []                # List of dicts

# Usage
user = UserProfile(
    name="Anil Kumar",
    email="anil@example.com",
    age=21,
    address={
        "street": "MG Road",
        "city": "Bangalore",
        "state": "Karnataka",
        "pin_code": "560001"
    },
    social={"github": "https://github.com/anil"},
    skills=["Python", "FastAPI", "Docker"],
    education=[
        {"degree": "B.Tech", "university": "VIT", "year": 2026}
    ]
)
```

### Deeply Nested — Multiple Levels

```python
class OrderItem(BaseModel):
    product_name: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(gt=0)

class ShippingInfo(BaseModel):
    address: Address  # Reuse Address model!
    delivery_type: str = "standard"

class Order(BaseModel):
    order_id: str
    customer_name: str
    items: list[OrderItem]      # List of nested models
    shipping: ShippingInfo       # Nested model
    total: float = Field(gt=0)

# FastAPI endpoint mein
@app.post("/orders/")
def create_order(order: Order):
    return {
        "message": f"Order {order.order_id} placed!",
        "items_count": len(order.items),
        "shipping_city": order.shipping.address.city
    }
```

---

## 2.5 ✨ Custom Validators

Jab built-in validation kaafi nahi ho, custom validators likhte hain.

### Field Validator (`@field_validator`)

```python
from pydantic import BaseModel, field_validator

class Student(BaseModel):
    name: str
    age: int
    email: str
    roll_number: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name khali nahi ho sakta!")
        return v.strip().title()  # "anil kumar" → "Anil Kumar"

    @field_validator("age")
    @classmethod
    def age_must_be_valid(cls, v: int) -> int:
        if v < 5 or v > 30:
            raise ValueError("Age 5 se 30 ke beech honi chahiye")
        return v

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Valid email do bhai!")
        return v.lower()

    @field_validator("roll_number")
    @classmethod
    def roll_must_be_uppercase(cls, v: str) -> str:
        return v.upper()
```

### Model Validator (`@model_validator`) — Multiple Fields Check

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date!")
        return self

class PasswordForm(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords match nahi kar rahe!")
        return self
```

### `mode="before"` — Raw Data Pe Validation

```python
class FlexibleInput(BaseModel):
    tags: list[str]

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v):
        # "python,fastapi,docker" → ["python", "fastapi", "docker"]
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",")]
        return v

# Dono chalenge:
FlexibleInput(tags=["python", "fastapi"])
FlexibleInput(tags="python, fastapi, docker")  # string bhi accept!
```

---

## 2.6 🔄 Model Inheritance & Variants

Production mein ek hi entity ke multiple versions chahiye (Create, Update, Response).

```python
class UserBase(BaseModel):
    """Common fields — sab models mein honge"""
    name: str
    email: str

class UserCreate(UserBase):
    """Signup ke liye — password bhi chahiye"""
    password: str

class UserUpdate(UserBase):
    """Update ke liye — sab optional"""
    name: str | None = None
    email: str | None = None

class UserInDB(UserBase):
    """DB se aaya data — id + hashed password"""
    id: int
    hashed_password: str
    is_active: bool = True

class UserResponse(UserBase):
    """API response — sensitive data nahi bhejenge"""
    id: int
    is_active: bool

# FastAPI endpoint
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # password hash karo, DB mein save karo
    db_user = {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "hashed_password": "hashed_" + user.password,
        "is_active": True
    }
    return db_user  # response_model filter karega
```

---

## 2.7 ⚙️ Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,   # " hello " → "hello"
        str_min_length=1,            # empty strings not allowed globally
        from_attributes=True,        # ORM models se bana sakte ho (SQLAlchemy)
        json_schema_extra={
            "examples": [
                {
                    "name": "iPhone 15",
                    "price": 79999.0,
                    "category": "electronics"
                }
            ]
        }
    )

    name: str
    price: float
    category: str
```

### `from_attributes=True` — SQLAlchemy Integration

```python
# SQLAlchemy model
class UserORM:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# Pydantic model with from_attributes
class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str

# ORM object → Pydantic model
orm_user = UserORM(id=1, name="Anil", email="anil@test.com")
pydantic_user = UserSchema.model_validate(orm_user)
```

---

## ⚠️ Common Mistakes

| # | Mistake | Solution |
|---|---------|----------|
| 1 | Pydantic v1 syntax use karna (`dict()`, `json()`) | v2 use karo: `model_dump()`, `model_dump_json()` |
| 2 | Mutable default values (`list` directly) | `Field(default_factory=list)` use karo |
| 3 | Validator mein value return nahi karna | `@field_validator` mein hamesha value return karo! |
| 4 | `Optional[str]` likhke default nahi dena | `Optional[str] = None` likho — default do |
| 5 | Sabhi fields ek hi model mein rakhna | Inheritance use karo: Base, Create, Update, Response |

---

## 💡 Pro Tips

1. **Pydantic v2 use karo** — v1 se 5x-50x faster hai
2. **`EmailStr`** use karo email validation ke liye: `pip install pydantic[email]`
3. **`HttpUrl`** use karo URL validation ke liye — Pydantic built-in types hai
4. **`model_config`** mein `str_strip_whitespace=True` daalo — whitespace issues khatam
5. **Separate models banao** — Create, Update, Response ke liye alag alag

---

## 🎯 Practice Exercise

**E-Commerce Product System:**

1. `ProductCreate` — name, price, category, description (optional)
2. `ProductUpdate` — sab optional
3. `ProductResponse` — id, name, price, category, created_at
4. Custom validators:
   - Name: min 3 chars, title case mein convert
   - Price: positive, max 10 lakh
   - Category: sirf predefined list mein se ho ("electronics", "clothing", "books")

---

> **Next Chapter:** [03 — Intermediate Concepts](./03_intermediate.md) →
