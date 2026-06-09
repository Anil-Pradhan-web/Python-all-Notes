# Q5. Share via Email

## Aim
To share a blog post through email using a form.

## Files Used
- `forms.py`
- `views.py`
- `templates/share.html`

## Code

### `forms.py`
```python
from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False)
```

### `views.py`
```python
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import EmailPostForm


def post_share(request):
    form = EmailPostForm(request.POST or None)

    if form.is_valid():
        send_mail(
            'Post Share',
            'Check this post',
            'sender@gmail.com',
            [form.cleaned_data['to']],
        )

    return render(request, 'share.html', {'form': form})
```

## Output
- Email sent successfully
