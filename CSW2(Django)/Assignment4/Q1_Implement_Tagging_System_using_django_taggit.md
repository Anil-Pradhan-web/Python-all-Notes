# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q1. Implement Tagging System using django-taggit

### Step 1: Install Package

```bash
pip install django-taggit
```

### Step 2: Add to `INSTALLED_APPS`

File: `content_project/settings.py` or your main project `settings.py`

```python
INSTALLED_APPS = [
    # ...
    'taggit',
]
```

### Step 3: Modify `Post` Model

File: `blog/models.py`

```python
from django.db import models
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    tags = TaggableManager()
```

### Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Register in Admin

File: `blog/admin.py`

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

### Output

- Admin panel shows the Tags field.
- Multiple tags can be added to a post.

Example:

```text
Post: Django Tutorial
Tags: django, python, web
```
