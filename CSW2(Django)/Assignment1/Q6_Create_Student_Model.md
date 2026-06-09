# Q6. Student Project

## Aim
To create a `Student` model.

## Files Used
- `models.py`
- `admin.py`

## Code

### `models.py`
```python
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name
```

### `admin.py`
```python
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

## Output
- Student added successfully via admin panel
