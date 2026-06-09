# Q2. Add Date Fields & Ordering

## Aim
To add `publish`, `created`, and `updated` fields in the `Post` model.

## Files Used
- `models.py`

## Code

### `models.py`
```python
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title
```

## Output
- Posts sorted by latest publish date
- Fields visible in admin
