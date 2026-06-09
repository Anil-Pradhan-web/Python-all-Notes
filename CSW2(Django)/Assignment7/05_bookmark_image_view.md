# Q5. Bookmark Image View

## Step 1: Create View

```python
from django.contrib import messages

@login_required
def image_create(request):

    if request.method == 'POST':

        form = ImageCreateForm(request.POST)

        if form.is_valid():

            new_item = form.save(commit=False)

            new_item.user = request.user

            new_item.save()

            messages.success(
                request,
                'Image added successfully'
            )

            return redirect(
                new_item.get_absolute_url()
            )

    else:
        form = ImageCreateForm()

    return render(
        request,
        'images/image/create.html',
        {'section': 'images', 'form': form}
    )
```

## Output

```text
Image bookmarked successfully
Success message displayed
```
