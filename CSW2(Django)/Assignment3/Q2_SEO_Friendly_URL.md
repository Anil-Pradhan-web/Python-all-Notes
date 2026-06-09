# Q2. SEO Friendly URL

## Aim
To create SEO-friendly URLs for blog post detail pages.

## Files Used
- `models.py`
- `urls.py`
- `views.py`

## Code

### `models.py`
```python
from django.db import models


class Post(models.Model):
    slug = models.SlugField(unique_for_date='publish')
```

### `urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        '<int:year>/<int:month>/<int:day>/<slug:slug>/',
        views.post_detail,
        name='post_detail',
    ),
]
```

### `views.py`
```python
from django.shortcuts import get_object_or_404, render
from .models import Post


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, 'post_detail.html', {'post': post})
```

## Output
- URL becomes: `/2026/04/05/post-title/`
