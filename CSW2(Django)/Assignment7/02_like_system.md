# Q2. Add Like System using ManyToManyField

## Step 1: Modify Model

```python
users_like = models.ManyToManyField(
    User,
    related_name='images_liked',
    blank=True
)
```

## Step 2: Register Model

```python
from django.contrib import admin
from .models import Image

admin.site.register(Image)
```

## Step 3: Apply Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

## Output

```text
Like/unlike relationship implemented successfully
```
