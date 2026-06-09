# Q3. Pagination

## Aim
To divide blog posts into pages using Django pagination.

## Files Used
- `views.py`
- `templates/pagination.html`

## Code

### `views.py`
```python
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(1)

    return render(request, 'post_list.html', {'posts': posts})
```

### `pagination.html`
```html
<div>
    {% if posts.has_previous %}
        <a href="?page={{ posts.previous_page_number }}">Previous</a>
    {% endif %}

    Page {{ posts.number }}

    {% if posts.has_next %}
        <a href="?page={{ posts.next_page_number }}">Next</a>
    {% endif %}
</div>
```

## Output
- Posts divided into pages with 3 posts per page
- Previous and Next navigation works correctly
