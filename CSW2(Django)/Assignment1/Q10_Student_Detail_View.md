# Q10. Student Detail View

## Aim
To display complete details of a single student.

## Files Used
- `views.py`
- `templates/studentApp/student_detail.html`

## Code

### `views.py`
```python
from django.shortcuts import render
from .models import Student


def student_detail(request, id):
    student = Student.objects.get(id=id)
    return render(request, 'studentApp/student_detail.html', {'student': student})
```

### `student_detail.html`
```html
<h1>{{ student.name }}</h1>
<p>{{ student.age }}</p>
```

## Output
- Student detail page opens successfully
