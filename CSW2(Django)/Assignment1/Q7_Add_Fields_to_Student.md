# Q7. Add Fields to Student

## Aim
To add more fields to the `Student` model.

## Files Used
- `models.py`

## Code

### `models.py`
```python
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll_number = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
```

## Output
- Students sorted alphabetically
- Roll number and created date stored for each student
