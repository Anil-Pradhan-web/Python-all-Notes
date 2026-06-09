# Q1. Create Images Application and Image Model

## Step 1: Create App
```bash
python manage.py startapp images
```

## Step 2: Add App in settings.py

```python
INSTALLED_APPS = [
    ...
    'images',
]
```

## Step 3: Create Image Model

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Image(models.Model):

    user = models.ForeignKey(
        User,
        related_name='images_created',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=200,
        blank=True
    )

    url = models.URLField()

    image = models.ImageField(
        upload_to='images/%Y/%m/%d'
    )

    description = models.TextField(blank=True)

    created = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
```

## Step 4: Apply Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

## Output

```text
Images application created
Automatic slug generation working
```
