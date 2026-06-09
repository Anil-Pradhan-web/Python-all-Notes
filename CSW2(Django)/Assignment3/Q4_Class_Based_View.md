# Q4. Class-Based View

## Aim
To display blog posts using Django class-based view.

## Files Used
- `views.py`
- `urls.py`

## Code

### `views.py`
```python
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post_list.html'
```

### `urls.py`
```python
from django.urls import path
from .views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
]
```

## Output
- Blog list displayed using class-based view
