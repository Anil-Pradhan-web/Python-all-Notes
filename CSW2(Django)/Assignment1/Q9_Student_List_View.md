# Q9. Student List View

## Aim
To display all students using a list view.

## Files Used
- `views.py`
- `templates/studentApp/student_list.html`

## Code

### `views.py`
```python
from django.shortcuts import render
from .models import Student


def student_list(request):
    students = Student.objects.all()
    return render(request, 'studentApp/student_list.html', {'students': students})
```

### `student_list.html`
```html
{% for s in students %}
    <p>{{ s.name }} - {{ s.age }}</p>
{% endfor %}
```

## Output
- `/students/` URL shows the student list
