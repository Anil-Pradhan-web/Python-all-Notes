# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q9. New Project `content_project`

### Steps

Create a new Django project and application:

```bash
django-admin startproject content_project
cd content_project
python manage.py startapp contentApp
```

### Model

Add the following model in `contentApp/models.py`:

File: `contentApp/models.py`

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()
    publish = models.DateTimeField()
```

### Output

- Articles can be created.
- Pagination works.
- Tagging system works.
