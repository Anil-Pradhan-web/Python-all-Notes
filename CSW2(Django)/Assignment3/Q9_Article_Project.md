# Q9. Article Project

## Aim
To create an `Article` model and display articles with pagination.

## Files Used
- `models.py`
- `views.py`
- `urls.py`

## Code

### `models.py`
```python
from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
```

### `views.py`
```python
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Article


def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 5)

    page = request.GET.get('page')
    articles = paginator.get_page(page)

    return render(request, 'article_list.html', {'articles': articles})
```

### `urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
]
```

## Output
- Articles displayed with pagination
