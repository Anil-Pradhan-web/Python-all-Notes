# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q7. Sitemap

### Step 1: Create Sitemap

Create a `sitemaps.py` file in the blog application:

File: `blog/sitemaps.py`

```python
from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
```

### Step 2: Configure URL

Add the sitemap URL in the project URL configuration:

File: `content_project/urls.py` or your main project `urls.py`

```python
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
```

### Output

```text
http://127.0.0.1:8000/sitemap.xml
```

The sitemap displays a list of all blog post URLs.
