# Q4. Download External Images

## Step 1: Install Requests

```bash
pip install requests
```

## Step 2: Override Save Method

```python
import requests
from django.core.files.base import ContentFile

def save(self, force_insert=False):

    image = super().save(commit=False)

    image_url = self.cleaned_data['url']

    response = requests.get(image_url)

    image_name = image_url.split('/')[-1]

    image.image.save(
        image_name,
        ContentFile(response.content),
        save=False
    )

    image.save()

    return image
```

## Output

```text
External image downloaded successfully
Image stored in media directory
```
