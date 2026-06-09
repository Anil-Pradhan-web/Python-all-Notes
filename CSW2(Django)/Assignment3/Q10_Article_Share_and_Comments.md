# Q10. Article Share + Comments

## Aim
To allow users to share and comment on articles.

## Files Used
- `forms.py`
- `models.py`

## Code

### `forms.py`
```python
from django import forms


class ArticleShareForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False)
```

### `models.py`
```python
from django.db import models


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
```

## Output
- Users can share and comment on articles
