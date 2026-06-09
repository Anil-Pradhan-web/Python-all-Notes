# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q5. Custom Template Tags

### Step 1: Create Folder

Create the following folder and files inside the `blog` application:

Files: `blog/templatetags/__init__.py` and `blog/templatetags/blog_tags.py`

```text
blog/
    templatetags/
        __init__.py
        blog_tags.py
```

### Step 2: Add Code

Add the following code in `blog/templatetags/blog_tags.py`:

File: `blog/templatetags/blog_tags.py`

```python
from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': posts}
```

### Step 3: Use in Template

File: `blog/templates/base.html` or any template where the sidebar/latest posts should be displayed.

```django
{% load blog_tags %}

Total posts: {% total_posts %}
{% show_latest_posts 3 %}
```

### Output

```text
Total posts: 10

Latest Posts:
- Post1
- Post2
- Post3
```
