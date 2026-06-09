# Q7. Comment Form

## Aim
To create a comment form using `ModelForm`.

## Files Used
- `forms.py`
- `views.py`

## Code

### `forms.py`
```python
from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
```

### `views.py`
```python
from .forms import CommentForm


def post_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()
```

## Output
- Comments submitted successfully
