# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q4. Display Similar Posts

### Step

Use tags to find posts that share similar tags with the current post:

File: `blog/views.py`

```python
from django.db.models import Count

post_tags_ids = post.tags.values_list('id', flat=True)

similar_posts = Post.published.filter(tags__in=post_tags_ids) \
    .exclude(id=post.id) \
    .annotate(same_tags=Count('tags')) \
    .order_by('-same_tags', '-publish')[:4]
```

### Output

```text
Similar Posts:
1. Django Forms Guide
2. Advanced Django ORM
3. Python Web Apps
```
