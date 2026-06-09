# Q1. Canonical URL

## Aim
To implement canonical URL using `get_absolute_url()`.

## Files Used
- `models.py`
- `templates/post_list.html`

## Code

### `models.py`
```python
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    publish = models.DateTimeField()

    def get_absolute_url(self):
        return reverse(
            'post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )
```

### `post_list.html`
```html
<a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
```

## Output
- Each post redirects to its detail page correctly
