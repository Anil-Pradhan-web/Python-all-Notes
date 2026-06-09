# Q6. Comment Model

## Aim
To create a `Comment` model for blog posts.

## Files Used
- `models.py`
- `admin.py`

## Code

### `models.py`
```python
from django.db import models


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
```

### `admin.py`
```python
from django.contrib import admin
from .models import Comment

admin.site.register(Comment)
```

## Output
- Comments visible in admin panel
