# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q3. Filter Posts by Tags

### Step 1: Update URL

File: `blog/urls.py`

```python
path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag')
```

### Step 2: Modify View

File: `blog/views.py`

```python
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag
from .models import Post

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    return render(request, 'blog/post/list.html', {
        'posts': posts,
        'tag': tag
    })
```

### Output

```text
URL: /tag/django/
```

- Shows only posts with the `django` tag.
- Invalid tag URL shows a 404 page.
