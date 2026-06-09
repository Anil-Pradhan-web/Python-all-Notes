# 🎯 CSW2 End Sem - Part 3: Auth, Social Login & Media (Assignment 5, 6, 7)
## Hinglish mein Poora Explanation Line by Line

---

# ========================================
# ASSIGNMENT 5: Authentication System
# ========================================

## Q1. Create Custom Login System

**Project Setup - Terminal mein**
```bash
django-admin startproject bookmarks   # Project banaya
cd bookmarks
python manage.py startapp account     # Auth ke liye alag app
```

**Login Form - File: `account/forms.py`**
```python
from django import forms

class LoginForm(forms.Form):
    """Yeh normal Form hai (ModelForm nahi) - kyunki User model se nahi linked"""
    username = forms.CharField()                       # Text input
    password = forms.CharField(widget=forms.PasswordInput)  # Password input (dots show)
    # PasswordInput widget = typing karte waqt *** dikhega
```

**Login View - File: `account/views.py`**
```python
from django.contrib.auth import authenticate, login
# authenticate = check karta hai username/password sahi hai ya nahi
# login = session create karta hai (user logged in ho jata hai)

def user_login(request):
    if request.method == 'POST':   # User ne form submit kiya
        form = LoginForm(request.POST)
        
        if form.is_valid():   # Saare fields valid hain?
            cd = form.cleaned_data   # cleaned_data = validated data dictionary
            
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            # authenticate returns User object if credentials correct, else None
            
            if user is not None:   # User mil gaya?
                login(request, user)   # User ko login karo
                return HttpResponse('Authenticated Successfully')
    
    else:   # GET request - form show karo
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})
```

**Flow:** Form → authenticate → login → success message

---

## Q2. Use LoginView and LogoutView

**Built-in views use karna - File: `account/urls.py`**
```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # LoginView auto handle karega form validation, authentication, login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

**Template Structure (Important - Specific folder name chahiye):**
```
templates/
    registration/          # Exactly yeh folder name
        login.html         # Login form template
        logged_out.html    # Logout ke baad dikhega
```

**Why built-in?** Kam code, tested, secure, aur features zyada

---

## Q3. Dashboard with login_required

**File: `account/views.py`**
```python
from django.contrib.auth.decorators import login_required

@login_required  # Decorator - iske bina logged in user bhi access nahi kar sakta
def dashboard(request):
    """Sirf logged in users ke liye accessible"""
    return render(request, 'account/dashboard.html')
```

**Settings mein redirect configure - File: `bookmarks/settings.py`**
```python
LOGIN_URL = 'login'            # Agar logged in nahi to yahan redirect kare
LOGIN_REDIRECT_URL = 'dashboard'  # Login ke baad yahan le jao
```

**@login_required kaam:**
1. Request aayi
2. Check kiya user authenticated hai?
3. Hai → view execute
4. Nahi → LOGIN_URL par redirect + next parameter (jahan bhejna tha)

---

## Q4. Password Change

**File: `account/urls.py`**
```python
urlpatterns = [
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(), 
         name='password_change'),
    # Form dikhata hai: old password + new password + confirm new password
    
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # Success message dikhata hai
]
```

**Templates:**
```
registration/password_change_form.html   # Form with old/new/confirm password
registration/password_change_done.html   # "Password changed successfully"
```

**Validation:** 
- New password != old password
- New password == confirm password
- Minimum length, complexity rules

---

## Q5. Password Reset

**Email backend - File: `bookmarks/settings.py`**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Console pe print karega email, production mein SMTP use karo
```

**URLs - File: `account/urls.py`**
```python
urlpatterns = [
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # User email dalta hai → token generate hota hai → email bhejta hai
]
```

**Flow:**
1. User email dalta hai
2. Django check karta hai email exists?
3. Token-based reset link generate karta hai (unique, time-limited)
4. Console pe link print karta hai
5. User link pe click karta hai
6. Token verify hota hai
7. Naya password set kar sakta hai

---

## Q6. User Registration System

**Registration Form - File: `account/forms.py`**
```python
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(forms.ModelForm):
    """ModelForm - User model se linked"""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    # Do password fields - ek main, ek confirm
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    
    def clean_password2(self):
        """Validation: dono passwords match? - clean_fieldname se Django auto call karega"""
        cd = self.cleaned_data
        
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
            # ValidationError = form valid nahi hoga, error dikhega
        
        return cd['password2']
```

**Registration View - File: `account/views.py`**
```python
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # commit=False - abhi database mein save mat karo
            # Kyunki password hash karna hai
            
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # set_password = password ko hash karta hai (encrypt)
            # Direct password assign nahi kar sakte (.password = '123' galat)
            # Hash = irreversible encryption
            new_user.save()  # Ab database mein save karo
    
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {'user_form': user_form})
```

---

## Q7. Profile Model (Extra User Info)

**User model mein extra fields add nahi kar sakte directly. To alag Profile model banate hain:**

**File: `account/models.py`**
```python
class Profile(models.Model):
    user = models.OneToOneField(
        User,                        # User model se link
        on_delete=models.CASCADE,    # User delete → Profile delete
    )
    date_of_birth = models.DateField(
        blank=True,    # Form mein optional
        null=True      # Database mein NULL allowed
    )
```

**OneToOneField:** Ek User ka ek hi Profile (like Aadhar card - ek insan ka ek)

**Command - Terminal mein**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Q8. Media Handling + Profile Image Upload

**Command - Terminal mein**
```bash
pip install Pillow
# Images ko process karne ke liye (resize, crop, etc.)
```

**Settings configure - File: `bookmarks/settings.py`**
```python
MEDIA_URL = '/media/'       # URL prefix for media files
MEDIA_ROOT = BASE_DIR / 'media'  # Disk par kahan store karna hai
```

**URLs mein serve karo - File: `bookmarks/urls.py`**
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
# Development mein Django media serve karega
# Production mein nginx/apache karega
```

**Profile model mein image add - File: `account/models.py`**
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',   # Folder structure: users/2026/06/05/
        blank=True
    )
```

**Template mein display - File: `templates/account/dashboard.html`**
```html
{% if user.profile.photo %}
    <img src="{{ user.profile.photo.url }}">   <!-- .url gives full URL -->
{% endif %}
```

---

## Q9-Q10. content_project with Authentication

**Combine all concepts:**
- Login/Logout (built-in views)
- User registration
- Profile model with image
- Profile edit form

**Profile Edit Form - File: `account/forms.py`**
```python
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']   # Sirf image field edit karo
```

**Edit View - File: `account/views.py`**
```python
@login_required
def edit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(
            request.POST,    # Text data
            request.FILES,   # File data (image)
            instance=request.user.profile   # Existing profile edit karo
        )
        if profile_form.is_valid():
            profile_form.save()
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'account/edit.html', {'profile_form': profile_form})
```

---

# ========================================
# ASSIGNMENT 6: Advanced Auth & Social Login
# ========================================

## Q1. Django Messages Framework

**View mein messages set karna - File: `account/views.py`**
```python
from django.contrib import messages

@login_required
def edit(request):
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully')
        # messages.success = green color success message
    else:
        messages.error(request, 'Error updating profile')
        # messages.error = red color error message
```

**Template mein display - File: `templates/account/edit.html`**
```html
{% if messages %}                    <!-- Koi message hai? -->
    <ul>
        {% for message in messages %}
            <li>{{ message }}</li>   <!-- Message dikhao -->
        {% endfor %}
    </ul>
{% endif %}
```

**Message types:**
- `messages.success()` → green
- `messages.error()` → red
- `messages.warning()` → yellow
- `messages.info()` → blue

---

## Q2. Email Authentication Backend

**Custom backend - email se login - File: `account/authentication.py`**
```python
class EmailAuthBackend:
    """Email address se authenticate karta hai"""
    
    def authenticate(self, request, username=None, password=None):
        """username parameter mein actual email aayega"""
        try:
            user = User.objects.get(email=username)  # Email se user dhundho
            if user.check_password(password):         # Password check karo
                return user                          # Sahi → user return
            return None                              # Galat → None
        except User.DoesNotExist:                    # Email nahi mila
            return None
    
    def get_user(self, user_id):
        """User ID se user return karo (session ke liye zaroori)"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

**Settings mein register - File: `bookmarks/settings.py`**
```python
AUTHENTICATION_BACKENDS = [
    'account.authentication.EmailAuthBackend',  # Custom - email se login
    'django.contrib.auth.backends.ModelBackend', # Default - username se login
]
```
**Order important:** Pehle custom, phir default - dono try karega

---

## Q3. Prevent Duplicate Email Registration

**Registration mein validation - File: `account/forms.py`**
```python
def clean_email(self):
    """Email already registered? Check karo"""
    data = self.cleaned_data['email']
    
    if User.objects.filter(email=data).exists():
        # .exists() = True/False return karta hai
        raise forms.ValidationError('Email already exists')
        # Error message form mein dikhega
    
    return data
```

**Edit form mein validation (current user ko exclude karna) - File: `account/forms.py`**
```python
def clean_email(self):
    data = self.cleaned_data['email']
    
    qs = User.objects.exclude(
        id=self.instance.id   # Current user ko exclude (uska email change allowed)
    ).filter(email=data)      # Baaki users mein email check
    
    if qs.exists():
        raise forms.ValidationError('Email already in use')
    
    return data
```

**Difference:** Registration mein sab users check, Edit mein current user exclude

---

## Q4. Python Social Auth (Social Login)

**Command - Terminal mein**
```bash
pip install social-auth-app-django
```

**Settings - File: `bookmarks/settings.py`**
```python
INSTALLED_APPS = [
    'social_django',   # Social auth app
]
```

**URLs - File: `bookmarks/urls.py`**
```python
path('social-auth/', include('social_django.urls', namespace='social'))
# /social-auth/login/google-oauth2/ etc.
```

**Authentication backends mein add karna - File: `bookmarks/settings.py`**
```python
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
```

---

## Q5. HTTPS Configuration

**Command - Terminal mein**
```bash
pip install django-extensions Werkzeug pyOpenSSL
# django-extensions = extra management commands
# Werkzeug = development server
# pyOpenSSL = SSL/TLS support
```

**Settings - File: `bookmarks/settings.py`**
```python
INSTALLED_APPS = [
    'django_extensions',
]

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

**Command - Terminal mein**
```bash
python manage.py runserver_plus --cert-file cert.crt
# HTTPS par chalega (https://127.0.0.1:8000)
```

---

## Q6. Google OAuth 2.0

**Environment variables - File: `bookmarks/settings.py`**
```python
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_SECRET')
```

**Backend add - File: `bookmarks/settings.py`**
```python
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',  # Google login
    'django.contrib.auth.backends.ModelBackend',  # Default login
]
```

**Kaise kaam karta hai:**
1. User "Login with Google" click karta hai
2. Google login page redirect hota hai
3. User Google credentials dalta hai
4. Google consent leta hai (permissions)
5. Google token bhejta hai Django ko
6. Django token verify karta hai
7. User logged in (ya new account create)

---

## Q7. Google Login Button

**File: `templates/registration/login.html`**
```html
<!-- login.html mein add -->
<a href="{% url 'social:begin' 'google-oauth2' %}">
    Sign in with Google
</a>
```

**Redirect after login - File: `bookmarks/settings.py`**
```python
LOGIN_REDIRECT_URL = 'dashboard'
```

---

## Q8. Custom Social Auth Pipeline

**Pipeline = Social login ke steps ka sequence**

**Create pipeline function - File: `account/pipeline.py`**
```python
def create_profile(strategy, details, user=None, *args, **kwargs):
    """Social login ke baad auto Profile create karo"""
    if user and not hasattr(user, 'profile'):
        # hasattr check karta hai user ke paas profile exists ya nahi
        Profile.objects.create(user=user)
```

**Settings mein pipeline configure - File: `bookmarks/settings.py`**
```python
SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',     # 1. User info lo
    'social_core.pipeline.social_auth.social_uid',         # 2. Unique ID banao
    'social_core.pipeline.social_auth.auth_allowed',       # 3. Allowed domain?
    'social_core.pipeline.social_auth.social_user',        # 4. Already registered?
    'social_core.pipeline.user.get_username',              # 5. Username banao
    'social_core.pipeline.user.create_user',               # 6. User create karo
    'account.pipeline.create_profile',                    # 7. Profile create karo (custom)
]
```

**Pipeline steps explain:**
- Each step ek function hai jo data process karta hai
- Step fail → pipeline stop (user login nahi hota)
- Custom step add kar sakte hain kahi bhi

---

## Q9. secureAuthProject (Practice Project)

**Command - Terminal mein**
```bash
django-admin startproject secureAuthProject
cd secureAuthProject
python manage.py startapp secureAuthApp
```

**.env file - File: `.env`**
```env
SECRET_KEY=mysecretkey
GOOGLE_KEY=mygooglekey
GOOGLE_SECRET=mygooglesecret
```

**Command - Terminal mein**
```bash
pip install python-dotenv
```

**File: `secureAuthProject/settings.py`**
```python
from dotenv import load_dotenv
import os

load_dotenv()   # .env file load karo

SECRET_KEY = os.getenv('SECRET_KEY')   # Environment variable read karo
```

**Why .env?** 
- `SECRET_KEY` = Django security key (critical)
- Google credentials = sensitive
- Git mein commit nahi karte (add to .gitignore)

---

## Q10. Advanced Social Auth (Multi-Provider)

**Multiple Providers (Google + GitHub) - File: `bookmarks/settings.py`**
```python
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',     # GitHub add
    'django.contrib.auth.backends.ModelBackend',
]
```

**GitHub Credentials - File: `bookmarks/settings.py`**
```python
SOCIAL_AUTH_GITHUB_KEY = os.getenv('GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('GITHUB_SECRET')
```

**Template mein - File: `templates/registration/login.html`**
```html
<a href="{% url 'social:begin' 'google-oauth2' %}">Sign in with Google</a>
<a href="{% url 'social:begin' 'github' %}">Sign in with GitHub</a>
```

**Output:** Users can login using Google OR GitHub

---

# ========================================
# ASSIGNMENT 7: Image Sharing & Media App
# ========================================

## Q1. Create Images Application and Image Model

**File: `images/models.py`**
```python
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Image(models.Model):
    user = models.ForeignKey(
        User,
        related_name='images_created',  # user.images_created.all()
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)  # Auto generate
    url = models.URLField()            # Image source URL
    image = models.ImageField(upload_to='images/%Y/%m/%d')  # Local copy
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """Save override - auto slug generate"""
        if not self.slug:
            self.slug = slugify(self.title)  # "My Image" → "my-image"
        super().save(*args, **kwargs)
```

**Command - Terminal mein**
```bash
python manage.py makemigrations
python manage.py migrate
```

**File: `images/admin.py`**
```python
from django.contrib import admin
from .models import Image

admin.site.register(Image)
```

---

## Q2. Add Like System (ManyToManyField)

**File: `images/models.py`**
```python
class Image(models.Model):
    # ...existing fields...
    users_like = models.ManyToManyField(
        User,
        related_name='images_liked',  # user.images_liked.all()
        blank=True
    )
```

**ManyToManyField:** Dono taraf se access:
- `image.users_like.all()` → image ko like karne wale users
- `user.images_liked.all()` → user ne jo images like ki hain

**ManyToMany ka table:** Django ek alag table banata hai (image_users_like)

---

## Q3. ImageCreateForm

**File: `images/forms.py`**
```python
from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        # image field nahi - download karenge
    
    def clean_url(self):
        """URL validation - sirf images allow"""
        url = self.cleaned_data['url']
        
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        # URL ka last part after . (e.g., image.jpg → jpg)
        
        if extension not in valid_extensions:
            raise forms.ValidationError('Unsupported file extension')
        
        return url
```

---

## Q4. Download External Images

**Command - Terminal mein**
```bash
pip install requests   # HTTP requests ke liye
```

**File: `images/forms.py` (ImageCreateForm mein save override)**
```python
import requests
from django.core.files.base import ContentFile

def save(self, force_insert=False):
    """Form save override - image download karo"""
    image = super().save(commit=False)  # Abhi save mat karo
    
    image_url = self.cleaned_data['url']
    response = requests.get(image_url)  # URL se image download
    # response.content = image bytes
    
    image_name = image_url.split('/')[-1]  # URL se filename lo
    
    image.image.save(
        image_name,                # Save as: photo.jpg
        ContentFile(response.content),  # File content
        save=False                 # Abhi full save mat karo
    )
    
    image.save()
    return image
```

**Flow:** URL → Download → Save to media/images/{year}/{month}/{day}/

---

## Q5. Bookmark Image View

**File: `images/views.py`**
```python
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user  # Current user assign
            new_item.save()               # Save + download trigger
            
            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
    
    else:
        form = ImageCreateForm()
    
    return render(request, 'images/image/create.html', 
                  {'section': 'images', 'form': form})
```

---

## Q6. JavaScript Bookmarklet

**Bookmarklet = Browser bookmark jo JavaScript execute kare**

**File: `templates/images/image/create.html`**
```html
<a href="javascript:
    var d=document,
    s=d.createElement('script');
    s.src='http://127.0.0.1:8000/static/js/bookmarklet.js';
    d.body.appendChild(s);">
    Bookmark it
</a>
```

**Kaam:** User is link ko bookmark kare → kisi bhi site pe click kare → tumhari site pe image bookmark kar sakta hai

---

## Q7. Dynamic Image Selection

**File: `static/js/bookmarklet.js`**
```javascript
// CSS dynamically load karo
var link = document.createElement('link');
link.rel = 'stylesheet';
link.href = '/static/css/bookmarklet.css';
document.head.appendChild(link);

// Saare images scan karo
var images = document.images;

for (var i = 0; i < images.length; i++) {
    if (images[i].width >= 100 && images[i].height >= 100) {
        // Sirf bade images dikhao (>= 100x100)
        console.log(images[i].src);
        // Overlay show karo user ko select karne ke liye
    }
}
```

---

## Q8. Image Detail + Like System

**get_absolute_url - File: `images/models.py`**
```python
from django.urls import reverse

def get_absolute_url(self):
    return reverse('images:detail', args=[self.id, self.slug])
    # /images/detail/1/my-image-slug/
```

**Detail View - File: `images/views.py`**
```python
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'image': image})
```

**Like/Unlike - File: `images/views.py`**
```python
# Like
image.users_like.add(request.user)    # User ko like list mein add

# Unlike
image.users_like.remove(request.user) # User ko like list se hataye
```

---

## Q9. Thumbnails + Infinite Scroll

**Command - Terminal mein**
```bash
pip install easy-thumbnails
```

**Settings - File: `bookmarks/settings.py`**
```python
INSTALLED_APPS = [
    'easy_thumbnails',
]
```

**Template mein thumbnail - File: `templates/images/image/detail.html`**
```html
{% load thumbnail %}

<img src="{% thumbnail image.image 300x300 %}" >
<!-- Auto 300x300 ka chhota image banayega (performance boost) -->
```

**Infinite Scroll JavaScript - File: `templates/images/image/list.html`**
```javascript
window.addEventListener('scroll', function() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        // User ne page bottom touch kiya
        console.log('Load more images');
        // AJAX call karo next page ke images lene ke liye
    }
});
```
- `window.innerHeight` = visible area height
- `window.scrollY` = kitna scroll kiya
- `document.body.offsetHeight` = total page height

---

## Q10. Advanced Content Sharing System (REST API)

**Command - Terminal mein**
```bash
pip install djangorestframework
```

**Serializer (JSON conversion) - File: `images/serializers.py`**
```python
from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    """Model ko JSON mein convert karo"""
    class Meta:
        model = Image
        fields = '__all__'   # Saare fields include
```

**API View - File: `images/views.py`**
```python
from rest_framework.generics import ListAPIView

class ImageListAPI(ListAPIView):
    """API endpoint - saari images JSON mein return"""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
```

**Features combined:**
- Image bookmarking
- Bookmarklet
- Like/unlike system
- Infinite scrolling
- AJAX image loading
- REST API integration

---

# ========================================
# QUICK REVISION - Key Points
# ========================================

**Authentication:**
- `authenticate()` → check credentials
- `login()` → create session
- `@login_required` → protect views
- `LoginView`, `LogoutView` → built-in

**Password:**
- `PasswordChangeView` → change password
- `PasswordResetView` → forgot password (token-based)
- `set_password()` → hash karna

**Registration:**
- `ModelForm` → User model se linked
- `clean_password2()` → password match validation
- `save(commit=False)` → modify before save

**Profile:**
- `OneToOneField(User)` → extra fields
- `ImageField(upload_to=...)` → image upload
- `MEDIA_URL`, `MEDIA_ROOT` → media configuration

**Messages:**
- `messages.success()` / `messages.error()`
- `{% for message in messages %}`

**Social Auth:**
- `social-auth-app-django` package
- Google OAuth2, GitHub OAuth2
- Pipeline (steps sequence)
- SOCIAL_AUTH_* settings

**Environment:**
- `python-dotenv` → .env files
- `os.getenv()` → read secrets

**Images App:**
- `slugify()` → auto slug
- `ManyToManyField` → likes
- `requests.get()` → download images
- `ContentFile` → save downloaded files

**Thumbnails:**
- `easy-thumbnails` → auto resize
- `{% thumbnail image 300x300 %}`

**Infinite Scroll:**
- `scroll` event listener
- Scroll position calculation
- AJAX load more

**REST API:**
- Django REST Framework
- `ModelSerializer` → model to JSON
- `ListAPIView` → list endpoint

---

# 🔥 EXAM KE LIYE IMPORTANT CODE SNIPPETS

**1. Custom Manager - File: `blog/models.py`**
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')
```

**2. Custom Authentication Backend - File: `account/authentication.py`**
```python
class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
```

**3. Social Auth Pipeline - File: `account/pipeline.py`**
```python
def create_profile(strategy, details, user=None, *args, **kwargs):
    if user and not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
```

**4. Image Download - File: `images/forms.py`**
```python
response = requests.get(image_url)
image.image.save(image_name, ContentFile(response.content), save=False)
```

**5. Model Form with File - File: `account/forms.py`**
```python
form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
```

**6. ManyToMany Like - File: `images/views.py`**
```python
image.users_like.add(request.user)    # Like
image.users_like.remove(request.user) # Unlike
```

**7. Tag Filtering - File: `blog/views.py`**
```python
posts = posts.filter(tags__in=[tag])
```

**8. Similar Posts - File: `blog/views.py`**
```python
similar_posts = Post.published.filter(tags__in=post_tags_ids)\
    .exclude(id=post.id)\
    .annotate(same_tags=Count('tags'))\
    .order_by('-same_tags')[:4]
```

**9. Messages - File: `account/views.py`**
```python
messages.success(request, 'Profile updated successfully')
messages.error(request, 'Error updating profile')
```

**10. Infinite Scroll - File: `templates/list.html`**
```javascript
window.addEventListener('scroll', function() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        // Load more
    }
});