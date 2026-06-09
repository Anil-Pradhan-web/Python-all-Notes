# Q6. JavaScript Bookmarklet

## Step 1: Add Bookmarklet Link

```html
<a href="javascript:
    var d=document,
    s=d.createElement('script');
    s.src='http://127.0.0.1:8000/static/js/bookmarklet.js';
    d.body.appendChild(s);">
    Bookmark it
</a>
```

## Output

```text
Bookmarklet launcher added to dashboard
```
