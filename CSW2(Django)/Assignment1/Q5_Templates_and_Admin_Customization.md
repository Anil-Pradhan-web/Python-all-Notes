# Q5. Templates + Admin Customization

## Aim
To create templates and customize the Django admin panel.

## Files Used
- `templates/base.html`
- `templates/blog/post_list.html`
- `templates/blog/post_detail.html`
- `admin.py`

## Code

### `base.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### `post_list.html`
```html
{% extends "base.html" %}

{% block content %}
    {% for post in posts %}
        <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
        <p>{{ post.body|truncatewords:30 }}</p>
    {% endfor %}
{% endblock %}
```

### `post_detail.html`
```html
{% extends "base.html" %}

{% block content %}
    <h1>{{ post.title }}</h1>
    <p>{{ post.body }}</p>
    <a href="/">Back</a>
{% endblock %}
```

### `admin.py`
```python
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish')
    list_filter = ('status', 'publish')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('status', 'publish')
```

## Output
- Blog list page and detail page working
- Admin panel enhanced with filters and search
