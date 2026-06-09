# Q7. Dynamic Image Selection Bookmarklet

## Step 1: Load CSS Dynamically

```javascript
var link = document.createElement('link');

link.rel = 'stylesheet';

link.href = '/static/css/bookmarklet.css';

document.head.appendChild(link);
```

## Step 2: Scan Images

```javascript
var images = document.images;

for (var i = 0; i < images.length; i++) {

    if (
        images[i].width >= 100 &&
        images[i].height >= 100
    ) {

        console.log(images[i].src);
    }
}
```

## Output

```text
Images scanned dynamically
Interactive image overlay displayed
```
