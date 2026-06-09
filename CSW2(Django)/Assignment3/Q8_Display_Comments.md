# Q8. Display Comments

## Aim
To display comments below each blog post.

## Files Used
- `templates/post_detail.html`

## Code

### `post_detail.html`
```html
{% for comment in comments %}
    <p>{{ comment.name }}: {{ comment.body }}</p>
{% endfor %}

{% include "comment_form.html" %}
```

## Output
- Comments displayed under each post
