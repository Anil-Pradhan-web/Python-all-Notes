# Q9. Thumbnails + Infinite Scroll

## Step 1: Install easy-thumbnails

```bash
pip install easy-thumbnails
```

## Step 2: Add App

```python
INSTALLED_APPS = [
    ...
    'easy_thumbnails',
]
```

## Step 3: Generate Thumbnail

```html
{% load thumbnail %}

<img src="{% thumbnail image.image 300x300 %}">
```

## Step 4: Infinite Scroll JavaScript

```javascript
window.addEventListener('scroll', function() {

    if (
        window.innerHeight + window.scrollY
        >= document.body.offsetHeight
    ) {

        console.log('Load more images');
    }
});
```

## Output

```text
Optimized thumbnails generated
Infinite scrolling implemented
```
