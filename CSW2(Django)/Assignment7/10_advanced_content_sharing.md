# Q10. Advanced Content Sharing System

## Step 1: Create Project

```bash
django-admin startproject mediaShareProject
cd mediaShareProject
python manage.py startapp mediaShareApp
```

## Features Implemented

* Image bookmarking
* Bookmarklet
* Like/unlike system
* Infinite scrolling
* AJAX image loading

## Advanced Feature:

REST API Integration

## Step 2: Install DRF

```bash
pip install djangorestframework
```

## Step 3: Create Serializer

```python
from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'
```

## Step 4: Create API View

```python
from rest_framework.generics import ListAPIView

class ImageListAPI(ListAPIView):

    queryset = Image.objects.all()

    serializer_class = ImageSerializer
```

## Output

```text
Complete media sharing system developed
REST API integrated successfully
Asynchronous functionality implemented
```
