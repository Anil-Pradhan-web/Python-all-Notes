# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q6. Markdown Support

### Step 1: Install Package

```bash
pip install markdown
```

### Step 2: Create Filter

Add the following code in the template tags file:

File: `blog/templatetags/blog_tags.py`

```python
import markdown
from django import template

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return markdown.markdown(text)
```

### Step 3: Use in Template

File: `blog/templates/blog/post/detail.html`

```django
{{ post.body|markdown }}
```

### Output

Input:

```markdown
**Hello**
```

Rendered:

```text
Hello
```

The word `Hello` is displayed in bold.
