# Q1. Create Blog Project & Post Model

## Aim
To create a Django project `college_blog` and app `blog` with a `Post` model.

## Files Used
- `models.py`
- `admin.py`

## Code

### `models.py`
```python
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()

    def __str__(self):
        return self.title
```

### `admin.py`
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

## Output
- `/admin/` page accessible
- Post successfully added
