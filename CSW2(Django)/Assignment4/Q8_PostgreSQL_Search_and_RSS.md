# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q8. PostgreSQL + Search + RSS

### Step 1: Configure PostgreSQL

Update the database configuration in `settings.py`:

File: `content_project/settings.py` or your main project `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
    }
}
```

### Step 2: Full-Text Search

Use PostgreSQL search features:

File: `blog/views.py` or the view where search functionality is implemented.

```python
from django.contrib.postgres.search import SearchVector

Post.objects.annotate(
    search=SearchVector('title', 'body')
).filter(search='django')
```

### Step 3: RSS Feed

Create a feed class:

File: `blog/feeds.py`

```python
from django.contrib.syndication.views import Feed
from .models import Post

class LatestPostsFeed(Feed):
    title = "Blog Posts"

    def items(self):
        return Post.published.all()[:5]
```

### Output

- Search returns relevant posts.
- RSS feed is available at:

```text
/feed/
```
