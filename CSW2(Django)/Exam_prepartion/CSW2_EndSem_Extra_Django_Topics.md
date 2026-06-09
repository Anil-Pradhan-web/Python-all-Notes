# 🎯 CSW2 End Sem - Extra Django Topics (Assignments se Bahar)
## Jo topics assignments mein nahi aaye par Exam mein aa sakte hain

---

# ========================================
# 1. Django Architecture - MTV Pattern
# ========================================

**Django follow karta hai MTV pattern:**
- **Model** → Database se baat karta hai (Tables, Queries)
- **Template** → Frontend HTML dikhata hai (User Interface)
- **View** → Logic handle karta hai (Business Logic)

```
User request → URL (urls.py) → View (views.py) → Model (models.py) → Database
                                                    ↓
User response ← Template (HTML) ← View ← Data
```

**MVC vs MTV (Interview mein puch sakte hain):**
| MVC | MTV |
|-----|-----|
| Model | Model (same) |
| View | Template |
| Controller | View |

Django mein "View" hi Controller ka kaam karta hai

---

# ========================================
# 2. Django ORM Deep - Q Objects & F Expressions
# ========================================

## Q Objects (Complex Queries - AND/OR/NOT)

**Problem:** Simple filter sirf AND karta hai
```python
# AND - dono conditions true honi chahiye
Post.objects.filter(status='PB', author=user)
# SQL: WHERE status='PB' AND author_id=1
```

**Q Objects se OR bhi kar sakte hain - File: `blog/views.py`**
```python
from django.db.models import Q

# OR - koi ek condition true
Post.objects.filter(
    Q(title__icontains='django') | Q(body__icontains='django')
)
# SQL: WHERE title LIKE '%django%' OR body LIKE '%django%'

# NOT - condition false honi chahiye
Post.objects.filter(~Q(status='DF'))
# ~ means NOT - SQL: WHERE status != 'DF'
# Yaani published posts

# Complex combinations
Post.objects.filter(
    Q(status='PB') & (Q(title__icontains='python') | Q(body__icontains='django'))
)
# Published posts jinme title mein python YA body mein django ho
```

## F Expressions (Field Value se Compare)

**Problem:** Ek field ki value doosri field se compare karni ho
```python
from django.db.models import F

# Comments count > posts count wale users
User.objects.filter(comments__gt=F('posts'))
# comments field ki value > posts field ki value

# Price badhao - har product ka price 10% increase
Product.objects.update(price=F('price') * 1.1)
# Ek hi query mein saare products ka price update

# Avoid race condition (thread-safe)
# F expression database level pe execute hota hai, Python mein nahi
```

---

# ========================================
# 3. Aggregation & Annotation
# ========================================

## Aggregation (Total values - poori query ke liye)
```python
from django.db.models import Count, Sum, Avg, Min, Max

# Total posts count
Post.objects.aggregate(Count('id'))
# Returns: {'id__count': 50}

# Named aggregation
Post.objects.aggregate(total=Count('id'), average_comments=Avg('comments__id'))
# Returns: {'total': 50, 'average_comments': 3.2}

# Sum of likes
Image.objects.aggregate(total_likes=Count('users_like'))
```

## Annotation (Har row ke liye extra field) - File: `blog/views.py`
```python
from django.db.models import Count

# Har post ke saath uske comments ka count
posts = Post.objects.annotate(comment_count=Count('comments'))
for post in posts:
    print(post.comment_count)  # Har post ke comments ka count

# Order by annotated field
posts = posts.order_by('-comment_count')[:5]  # Top 5 most commented

# Multiple annotations
posts = Post.objects.annotate(
    comment_count=Count('comments'),
    like_count=Count('likes')
)
```

**Aggregate vs Annotate:**
| Aggregate | Annotate |
|-----------|----------|
| Ek value return karta hai | Har row mein field add karta hai |
| Dictionary return | QuerySet return |
| `aggregate(Count('id'))` | `annotate(count=Count('id'))` |

---

# ========================================
# 4. Django Middleware
# ========================================

**Middleware = Request/Response ke beech mein processing layer**

```
Request → Middleware 1 → Middleware 2 → View → Middleware 2 → Middleware 1 → Response
```

**Built-in Middleware - File: `settings.py`**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',     # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sessions
    'django.middleware.common.CommonMiddleware',          # Common
    'django.middleware.csrf.CsrfViewMiddleware',         # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth
    'django.contrib.messages.middleware.MessageMiddleware',     # Messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjack protection
]
```

**Custom Middleware Banana - File: `myapp/middleware.py`**
```python
import time

class RequestTimerMiddleware:
    """Request ka time calculate karta hai"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Request processing se pehle
        start_time = time.time()
        
        response = self.get_response(request)  # View call
        
        # Request processing ke baad
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Request took {duration:.2f} seconds")
        
        return response
```

**Settings mein register - File: `settings.py`**
```python
MIDDLEWARE = [
    'myapp.middleware.RequestTimerMiddleware',
    # ... other middleware
]
```

---

# ========================================
# 5. Django Signals
# ========================================

**Signals = Jab kuch hota hai to notification bhejta hai**

**Common Built-in Signals:**
- `pre_save` / `post_save` → Save karne se pehle/baad
- `pre_delete` / `post_delete` → Delete karne se pehle/baad
- `m2m_changed` → ManyToMany field change hone par
- `user_logged_in` / `user_logged_out` → Login/Logout par

**Example - Post save hone par log karo - File: `blog/signals.py`**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def post_saved_handler(sender, instance, created, **kwargs):
    """Jab bhi Post save ho, yeh function run hoga"""
    if created:
        print(f"New post created: {instance.title}")
    else:
        print(f"Post updated: {instance.title}")
```

**App ready karna - File: `blog/apps.py`**
```python
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        import blog.signals  # signals import karo
```

**Kyun use karte hain?**
- Profile auto-create karna jab user register kare
- Activity log maintain karna
- Cache clear karna jab data change ho
- Email send karna event par

---

# ========================================
# 6. Sessions Framework
# ========================================

**Session = Ek user ke multiple requests ke beech data store karna**

**Session store types:**
- Database (default) - `django.contrib.sessions.backends.db`
- Cache - `django.contrib.sessions.backends.cache`
- File - `django.contrib.sessions.backends.file`
- Cookie - `django.contrib.sessions.backends.signed_cookies`

**Session use karna - File: `blog/views.py`**
```python
# View mein session set karo
def add_to_cart(request):
    request.session['cart'] = ['item1', 'item2']  # Session mein save
    request.session['user_preferences'] = {'theme': 'dark', 'lang': 'hi'}
    
    # Session expiry
    request.session.set_expiry(3600)  # 1 hour mein expire

# Session read karo
def show_cart(request):
    cart = request.session.get('cart', [])  # Default value [] agar nahi hai
    theme = request.session.get('user_preferences', {}).get('theme')
    
# Session delete karo
def logout(request):
    request.session.flush()  # Poori session delete
```

**Session key vs Cookie:**
```
Cookie (Browser)              Session (Server)
┌─────────────────┐           ┌──────────────────┐
│ sessionid: abc123│ ─────── → │ abc123: cart data │
└─────────────────┘           └──────────────────┘
```
Browser mein sirf session ID store, actual data server pe

---

# ========================================
# 7. Custom User Model
# ========================================

**Problem:** Default User model mein sirf specific fields hain (username, email, etc.)
**Agar aapko phone_number, address jaise fields chahiye to do tarike hain**

## Option 1: OneToOneField (Profile model - Already Assignments mein kiya)
## Option 2: Custom User Model (AbstractUser / AbstractBaseUser)

**AbstractUser (Default User ko extend karo) - File: `myapp/models.py`**
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Default User mein extra fields add karo"""
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.email
```

**AbstractBaseUser (Poore naye User model - Advanced) - File: `myapp/models.py`**
```python
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'  # Login email se
    REQUIRED_FIELDS = ['name']
```

**Settings mein batana zaroori - File: `settings.py`**
```python
AUTH_USER_MODEL = 'myapp.CustomUser'
# Migration se PEHLE yeh set karo
```

---

# ========================================
# 8. Django Admin - Advanced Features
# ========================================

## Custom Admin Actions (Bulk operations) - File: `blog/admin.py`
```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish', 'view_count')
    list_filter = ('status', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    
    # Custom action
    actions = ['make_published', 'make_draft']
    
    @admin.action(description='Mark selected posts as published')
    def make_published(self, request, queryset):
        """Selected posts ko publish karo"""
        updated = queryset.update(status='PB')
        self.message_user(request, f'{updated} posts published')
    
    @admin.action(description='Mark selected posts as draft')
    def make_draft(self, request, queryset):
        updated = queryset.update(status='DF')
        self.message_user(request, f'{updated} posts moved to draft')
    
    # Custom fields
    def view_count(self, obj):
        return obj.comments.count()
    view_count.short_description = 'Comments'
```

## Inline Models (Parent-child ek sath edit) - File: `blog/admin.py`
```python
class CommentInline(admin.TabularInline):  # ya StackedInline
    model = Comment
    extra = 1  # Kitne empty forms dikhane hain

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]  # Post edit karte waqt comments bhi edit
```

## Fieldsets (Form ko groups mein divide) - File: `blog/admin.py`
```python
fieldsets = (
    ('Post Content', {
        'fields': ('title', 'slug', 'body')
    }),
    ('Publishing', {
        'fields': ('status', 'publish', 'author')
    }),
    ('Meta', {
        'fields': ('tags',),
        'classes': ('collapse',)  # Collapsible section
    }),
)
```

---

# ========================================
# 9. Testing in Django
# ========================================

**File: `blog/tests.py`**
```python
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        """Har test se pehle run hota hai"""
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            body='Test body'
        )
    
    def test_post_creation(self):
        """Test: Post create ho raha hai?"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertTrue(isinstance(self.post, Post))
    
    def test_post_str_method(self):
        """Test: __str__ method sahi hai?"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_list_view(self):
        """Test: View sahi response de raha hai?"""
        client = Client()
        response = client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_view(self):
        """Test: Detail view 404 de raha hai?"""
        response = self.client.get('/post/9999/')
        self.assertEqual(response.status_code, 404)
```

**Commands:**
```bash
python manage.py test                    # Saare tests run
python manage.py test blog               # Sirf blog app
python manage.py test blog.tests.PostModelTest  # Specific test class
python manage.py test --verbosity=2      # Detailed output
```

---

# ========================================
# 10. Django REST Framework (DRF) - Advanced
# ========================================

## ViewSets & Routers - File: `images/views.py`
```python
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):  # CRUD sab auto!
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes.add(request.user)
        return Response({'status': 'liked'})
    
    @action(detail=False)
    def recent(self, request):
        posts = Post.objects.all()[:5]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
```

**URLs - Automatic Routing - File: `bookmarks/urls.py`**
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Auto: GET, POST, PUT, DELETE
]
```

**Permissions - File: `images/views.py`**
```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Sirf logged in users
    # IsAdminUser → sirf staff
    # AllowAny → sab
```

---

# ========================================
# 11. Caching in Django
# ========================================

**Cache = Frequently used data ko temporarily store karna (fast access)**

**Cache Backends:**
- `Memcached` - Fastest, production mein use hota hai
- `Redis` - Popular, multi-purpose
- `Database` - Simple, dev ke liye
- `File` - File system mein store
- `Dummy` - Development, actually cache nahi karta

**Per-View Caching - File: `blog/views.py`**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes cache
def post_list(request):
    # ... heavy query ...
    return render(...)
```

**Template Caching - File: `templates/blog/post/list.html`**
```html
{% load cache %}

{% cache 300 sidebar %}
    {% show_latest_posts 5 %}
    {% total_posts %}
{% endcache %}
```

**Low-level Cache API - File: `blog/views.py`**
```python
from django.core.cache import cache

# Set cache
cache.set('total_posts', 50, 300)  # Key, Value, Timeout

# Get cache
total = cache.get('total_posts')

# Agar cache mein nahi to compute karo
total = cache.get_or_set('total_posts', Post.objects.count(), 300)

# Delete cache
cache.delete('total_posts')
```

---

# ========================================
# 12. Django Security
# ========================================

**CSRF Attack Protection - File: `templates/*.html`**
```python
# {% csrf_token %} - Har form mein dalna mandatory
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
# CSRF token verify karta hai ki request humare site se aayi hai
```

**XSS (Cross-Site Scripting):**
```python
# Django auto-escape karta hai template variables
{{ user_input }}  # <script> tag bhi safe show hoga
{{ user_input|safe }}  # Agar trusted ho tabhi use karo
```

**SQL Injection:**
```python
# Django ORM auto-escapes (safe)
Post.objects.filter(title=user_input)  # Safe

# Raw SQL (dangerous)
Post.objects.raw(f"SELECT * FROM post WHERE title = '{user_input}'")  # ❌
Post.objects.raw("SELECT * FROM post WHERE title = %s", [user_input])  # ✅
```

**Security Settings - File: `settings.py`**
```python
SECURE_SSL_REDIRECT = True       # HTTP → HTTPS redirect
SECURE_HSTS_SECONDS = 31536000   # Always HTTPS
SECURE_BROWSER_XSS_FILTER = True # XSS protection
X_FRAME_OPTIONS = 'DENY'         # Clickjacking protection
CSRF_COOKIE_SECURE = True        # CSRF cookie only HTTPS
SESSION_COOKIE_SECURE = True     # Session cookie only HTTPS
```

---

# ========================================
# 13. Django Management Commands
# ========================================

**Custom command banana - Folder Structure:**
```
myapp/
    management/
        __init__.py
        commands/
            __init__.py
            import_posts.py
```

**File: `myapp/management/commands/import_posts.py`**
```python
from django.core.management.base import BaseCommand
from blog.models import Post

class Command(BaseCommand):
    help = 'Import posts from CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='CSV file path')
        parser.add_argument('--dry-run', action='store_true', help='Test run')
    
    def handle(self, *args, **options):
        file_path = options['file_path']
        dry_run = options['dry_run']
        
        self.stdout.write(f'Importing from {file_path}...')
        
        # ... import logic ...
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Dry run - no changes made'))
        else:
            self.stdout.write(self.style.SUCCESS('Import successful!'))
```

**Run:**
```bash
python manage.py import_posts data.csv
python manage.py import_posts data.csv --dry-run
```

---

# ========================================
# 14. Django Migrations - Advanced
# ========================================

**Data Migration (Data bhi migrate karo):**
```bash
python manage.py makemigrations blog --empty
# Empty migration file banega, usme code likho
```

**File: `blog/migrations/0003_auto_data_migration.py`**
```python
from django.db import migrations

def set_default_status(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    Post.objects.filter(status=None).update(status='DF')

class Migration(migrations.Migration):
    dependencies = [('blog', '0002_...')]
    operations = [
        migrations.RunPython(set_default_status),
    ]
```

**Migration Commands:**
```bash
python manage.py showmigrations          # Migration status
python manage.py migrate blog 0002       # Specific migration tak jao
python manage.py migrate blog zero        # Sab undo karo
python manage.py sqlmigrate blog 0003    # SQL dekh lo
```

**Migration Squashing (Combine karna):**
```bash
python manage.py squashmigrations blog 0005
# 1-5 migrations ko ek mein combine karega
```

---

# ========================================
# 15. Context Processors
# ========================================

**Kya hai?** Har template mein by default kuch variables available karwana

**File: `myapp/context_processors.py`**
```python
from .models import Category

def categories_processor(request):
    """Har template mein categories available honge"""
    return {
        'all_categories': Category.objects.all(),
        'recent_posts_count': Post.published.count(),
    }
```

**Settings mein register - File: `settings.py`**
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'myapp.context_processors.categories_processor',
                # ... default processors
            ],
        },
    },
]
```

**Ab har template mein use kar sakte ho - File: `templates/base.html`**
```html
{% for cat in all_categories %}
    <a href="{% url 'category' cat.slug %}">{{ cat.name }}</a>
{% endfor %}
<p>Total posts: {{ recent_posts_count }}</p>
```

**Default Context Processors:**
- `django.template.context_processors.request` → `{{ request }}`
- `django.contrib.auth.context_processors.auth` → `{{ user }}`
- `django.contrib.messages.context_processors.messages` → `{{ messages }}`

---

# ========================================
# 16. Static Files Management
# ========================================

**Settings - File: `settings.py`**
```python
STATIC_URL = '/static/'          # URL prefix
STATICFILES_DIRS = [BASE_DIR / 'static']  # Development folder
STATIC_ROOT = BASE_DIR / 'staticfiles'    # Production collect location
```

**Template mein - File: `templates/base.html`**
```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
<img src="{% static 'images/logo.png' %}">
```

**Production mein:**
```bash
python manage.py collectstatic
# Saare static files ko STATIC_ROOT mein collect karo
# (Nginx/Apache serve karega)
```

**Static vs Media:**
| Static Files | Media Files |
|--------------|-------------|
| CSS, JS, Images (theme) | User uploads (photos, files) |
| `STATIC_URL = '/static/'` | `MEDIA_URL = '/media/'` |
| `collectstatic` se ek jagah | Direct user upload |
| Part of codebase | User-generated |

---

# ========================================
# 17. Django Formsets & Inline Formsets
# ========================================

**Formset = Ek page par ek saath multiple forms**

**File: `blog/views.py`**
```python
from django.forms import formset_factory
from .forms import CommentForm

# 3 forms ka formset
CommentFormSet = formset_factory(CommentForm, extra=3)

def manage_comments(request, post_id):
    if request.method == 'POST':
        formset = CommentFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                comment = form.save(commit=False)
                comment.post_id = post_id
                comment.save()
    else:
        formset = CommentFormSet()
    
    return render(request, 'manage_comments.html', {'formset': formset})
```

**Template mein - File: `templates/manage_comments.html`**
```html
<form method="post">
    {% csrf_token %}
    {{ formset.management_form }}  <!-- Required hidden fields -->
    {% for form in formset %}
        <div class="comment-form">
            {{ form.as_p }}
        </div>
    {% endfor %}
    <button type="submit">Save All</button>
</form>
```

**Model Formset (Model se linked) - File: `blog/views.py`**
```python
from django.forms import modelformset_factory

CommentFormSet = modelformset_factory(Comment, fields=('name', 'body'), extra=3)
```

---

# ========================================
# 18. Django Logging
# ========================================

**File: `settings.py`**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'myapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**Use in code - File: `blog/views.py`**
```python
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug('This is debug message')
    logger.info('View called with user: %s', request.user)
    logger.warning('Something suspicious')
    logger.error('Something went wrong!')
```

---

# ========================================
# 19. Django File Upload (Advanced)
# ========================================

**File: `myapp/models.py`**
```python
class Document(models.Model):
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

**File: `myapp/views.py`**
```python
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # FILES mandatory
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})

# Validation
def clean_file(self):
    file = self.cleaned_data['file']
    if file.size > 5 * 1024 * 1024:  # 5MB limit
        raise forms.ValidationError('File too large')
    if not file.name.endswith('.pdf'):
        raise forms.ValidationError('Only PDF allowed')
    return file
```

---

# ========================================
# 20. Django Deployment Basics
# ========================================

**Production Checklist - File: `settings.py`**
```python
DEBUG = False  # ❌ Kabhi True mat rakho production mein
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database - PostgreSQL recommended
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    }
}

# Static/Media files
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**WSGI (Web Server Gateway Interface) - File: `wsgi.py`**
```python
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_wsgi_application()
```

**ASGI (Async - Channels ke liye) - File: `asgi.py`**
```python
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_asgi_application()
```

**Hosting Options:**
- PythonAnywhere (beginner friendly)
- Heroku (easy but paid)
- DigitalOcean / Vultr (VPS)
- AWS Elastic Beanstalk
- Railway / Render

---

# ========================================
# 🔥 EXAM KE LIYE TOP IMPORTANT SNIPPETS
# ========================================

**1. Q Objects - OR Query - File: `blog/views.py`**
```python
from django.db.models import Q
results = Model.objects.filter(Q(field1='val') | Q(field2='val'))
```

**2. F Expression - Field compare - File: `blog/views.py`**
```python
from django.db.models import F
Model.objects.filter(field1__gt=F('field2'))
```

**3. Aggregation - File: `blog/views.py`**
```python
from django.db.models import Count, Sum, Avg
Model.objects.aggregate(total=Count('id'))
```

**4. Annotation - File: `blog/views.py`**
```python
Model.objects.annotate(count=Count('related_field'))
```

**5. Signals - File: `blog/signals.py`**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=Model)
def handler(sender, instance, created, **kwargs):
    pass
```

**6. Middleware - File: `myapp/middleware.py`**
```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        return self.get_response(request)
```

**7. Session - File: `blog/views.py`**
```python
request.session['key'] = 'value'
request.session.get('key', default)
```

**8. Cache - File: `blog/views.py`**
```python
from django.core.cache import cache
cache.set('key', 'value', timeout)
cache.get('key')