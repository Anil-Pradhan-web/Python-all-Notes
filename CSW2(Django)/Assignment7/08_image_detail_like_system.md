# Q8. Image Detail + Like System

## Step 1: Add get_absolute_url()

```python
from django.urls import reverse

def get_absolute_url(self):

    return reverse(
        'images:detail',
        args=[self.id, self.slug]
    )
```

## Step 2: Create Detail View

```python
def image_detail(request, id, slug):

    image = get_object_or_404(
        Image,
        id=id,
        slug=slug
    )

    return render(
        request,
        'images/image/detail.html',
        {'image': image}
    )
```

## Step 3: Like/Unlike

```python
image.users_like.add(request.user)
image.users_like.remove(request.user)
```

## Output

```text
Image detail page working
Like/unlike system functioning properly
```
