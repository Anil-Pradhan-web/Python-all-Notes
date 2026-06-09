# Q3. Create ImageCreateForm

## Step 1: Create Form

```python
from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['title', 'url', 'description']

    def clean_url(self):

        url = self.cleaned_data['url']

        valid_extensions = ['jpg', 'jpeg', 'png']

        extension = url.rsplit('.', 1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError(
                'Unsupported file extension'
            )

        return url
```

## Output

```text
Only jpg, jpeg, png files accepted
Invalid formats rejected
```
