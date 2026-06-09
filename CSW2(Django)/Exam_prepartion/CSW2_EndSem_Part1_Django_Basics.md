# 🎯 CSW2 End Sem - Part 1: Django Basics (Assignment 1, 2, 3)
## Hinglish mein Poora Explanation Line by Line

---

# ========================================
# ASSIGNMENT 1: Django Framework Basics
# ========================================

## Q1. Create Blog Project & Post Model

**Kya hai yeh?**
- Django ka project banate hain `college_blog` naam ka
- Uske andar ek app banate hain `blog` naam ka
- `Post` model banate hain jo database ki table banegi

**Code Samajh - File: `blog/models.py`**
```python
from django.db import models

class Post(models.Model):   # models.Model se inherit kiya - iska matlab yeh database table banega
    title = models.CharField(max_length=250)   # CharField = text field, max_length=250 means 250 characters tak
    slug = models.SlugField(max_length=250)     # SlugField = URL-friendly text (no spaces, special chars)
    body = models.TextField()                   # TextField = bada text field, koi limit nahi
```
- `__str__(self)` → Object ko print karega to title dikhega, nahi to `Post object(1)` dikhega

**Admin mein register - File: `blog/admin.py`**
```python
admin.site.register(Post)   # Isse Post model admin panel mein dikhega
```

**Output:** `/admin/` pe jaake Post add kar sakte ho

---

## Q2. Add Date Fields & Ordering

**Naye fields add kiye - File: `blog/models.py`**
```python
from django.utils import timezone

publish = models.DateTimeField(default=timezone.now)
    # DateTimeField = date + time store karta hai
    # default=timezone.now = jab naya post bane to current time auto set ho jaye

created = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True = sirf pehli baar jab create ho tab time set hoga, badme change nahi hoga

updated = models.DateTimeField(auto_now=True)
    # auto_now=True = har baar jab bhi save karega to current time set hoga
```

**Meta class (ordering) - File: `blog/models.py`**
```python
class Meta:
    ordering = ['-publish']   # '-' means descending order, latest publish wala pehle aayega
    indexes = [
        models.Index(fields=['publish']),   # Index = search fast karne ke liye
    ]
```
- Meta class model ke baare mein metadata (settings) batati hai
- Index database mein query ko fast karta hai

---

## Q3. Status & Author

**Status field with choices - File: `blog/models.py`**
```python
class Status(models.TextChoices):
    DRAFT = 'DF', 'Draft'      # DF database me store hoga, Draft admin me dikhega
    PUBLISHED = 'PB', 'Published'  # PB store hoga, Published dikhega

status = models.CharField(
    max_length=2,
    choices=Status.choices,     # choices = dropdown banega admin mein
    default=Status.DRAFT,       # default = 'DF' (Draft)
)
```

**Author ForeignKey - File: `blog/models.py`**
```python
author = models.ForeignKey(
    settings.AUTH_USER_MODEL,    # User model se link kiya (ForeignKey = many-to-one relation)
    on_delete=models.CASCADE,    # CASCADE = agar user delete hua to uske posts bhi delete
    related_name='blog_posts',   # related_name = reverse query ke liye (user.blog_posts.all())
)
```
- ForeignKey = ek Post ka ek Author hota hai, but ek Author ke multiple Posts ho sakte hain
- `on_delete=models.CASCADE` - parent delete to child bhi delete

---

## Q4. Custom Manager + Views + URLs

**Custom Manager (sirf published posts dikhane ke liye) - File: `blog/models.py`**
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')
        # super().get_queryset() = sab posts lo
        # .filter(status='PB') = sirf wahi jinka status 'PB' (Published) hai

# Model mein dono managers:
objects = models.Manager()       # default manager, sab kuch dikhata
published = PublishedManager()   # custom manager, sirf published
```
Ab: `Post.published.all()` → sirf published posts
     `Post.objects.all()` → sab posts (draft bhi)

**get_absolute_url (SEO-friendly URL) - File: `blog/models.py`**
```python
def get_absolute_url(self):
    return reverse('post_detail', args=[
        self.publish.year,
        self.publish.month,
        self.publish.day,
        self.slug,
    ])
    # URL banega: /2026/6/5/my-post-slug/
    # reverse = URL name se URL generate karta hai
```

**Views (function-based) - File: `blog/views.py`**
```python
def post_list(request):
    posts = Post.published.all()   # sirf published posts
    return render(request, 'blog/post_list.html', {'posts': posts})
    # render = template + data ko milakar HTML bana ke bhejta hai

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, publish__year=year, ...)
    # get_object_or_404 = mila to return, nahi to 404 error
    return render(request, 'blog/post_detail.html', {'post': post})
```

**URLs - File: `blog/urls.py`**
```python
path('', views.post_list, name='post_list'),
path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    # <int:year> = integer capture karega, <slug:slug> = slug capture karega
```

---

## Q5. Templates & Admin Customization

**Template Inheritance - File: `templates/base.html`**
```html
<!-- base.html - sabse upar wala template -->
{% block content %}{% endblock %}   <!-- child templates yahan bhar sakte hain -->
```

**Template - File: `templates/blog/post_list.html`**
```html
{% extends "base.html" %}    <!-- base.html se inherit kiya -->
{% block content %}
    {{ post.body|truncatewords:30 }}   <!-- truncatewords:30 = sirf 30 words dikhao -->
{% endblock %}
```

**Template - File: `templates/blog/post_detail.html`**
```html
{% extends "base.html" %}
{% block content %}
    <h1>{{ post.title }}</h1>
    <p>{{ post.body }}</p>
    <a href="/">Back</a>
{% endblock %}
```

**Admin Customization - File: `blog/admin.py`**
```python
@admin.register(Post)   # decorator se register kiya
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish')   # admin list mein ye columns dikhe
    list_filter = ('status', 'publish')             # filter sidebar
    search_fields = ('title', 'body')               # search box
    prepopulated_fields = {'slug': ('title',)}      # title likhte hi slug auto fill
    ordering = ('status', 'publish')                # default ordering
```

---

## Q6-Q10. Student Model (CRUD Practice)

**Student Model - File: `studentApp/models.py`**
```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll_number = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']   # A to Z order
```

**Department Relation (ForeignKey) - File: `studentApp/models.py`**
```python
class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    dept_code = models.CharField(max_length=10)

class Student(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='students',   # department.students.all() se saare students milenge
    )
```

**Student List & Detail Views - File: `studentApp/views.py`**
```python
# List - saare students
students = Student.objects.all()

# Detail - ek specific student
student = Student.objects.get(id=id)   # id se uthaya
```

**Template - File: `studentApp/templates/studentApp/student_list.html`**
```html
{% for s in students %}
    <p>{{ s.name }} - {{ s.age }}</p>
{% endfor %}
```

---

# ========================================
# ASSIGNMENT 2: HTML & CSS (Frontend Basics)
# ========================================

## Basic HTML Structure

**Headings & Text:**
- `<h1>` - sabse bada heading (page ka title)
- `<h2>` - chota heading (section title)
- `<p>` - paragraph text
- `<ul>` / `<ol>` - unordered/ordered list
- `<li>` - list item

**Tables - File: `q3_student_report.html` / `q8_styled_table.html`**
```html
<table>
    <tr>        <!-- table row -->
        <th>Name</th>   <!-- table header (bold) -->
        <th>Age</th>
    </tr>
    <tr>
        <td>Anil</td>   <!-- table data -->
        <td>20</td>
    </tr>
</table>
```

**Images - File: `q2_image_gallery.html`**
```html
<img src="photo.jpg" alt="Description" width="200">
<!-- src = image file path, alt = agar image na dikhe to ye text dikhe -->
```

---

## CSS Types (3 Tarah ke)

**1. Inline CSS** - Direct element mein:
```html
<h1 style="color: red; font-size: 24px;">Hello</h1>
```

**2. Internal CSS** - Head section mein - File: `q7_css_types.html`
```html
<head>
    <style>
        h1 { color: blue; }
        p { font-size: 16px; }
    </style>
</head>
```

**3. External CSS (Best Practice)** - Alag file mein - File: `style.css`
```css
/* style.css */
h1 { color: green; }
p { font-size: 14px; }
```
HTML mein link karo - File: `q7_css_types.html`
```html
<link rel="stylesheet" href="style.css">
```

**Hover Effect - File: `q9_hover_background.html` / `style.css`**
```css
button:hover {
    background-color: yellow;
    /* Jab mouse button par aayega to yellow ho jayega */
}
```

---

# ========================================
# ASSIGNMENT 3: Advanced Django Logic
# ========================================

## Q1-Q2. Canonical & SEO-Friendly URLs

**Problem:** URL `/post/12/` se user ko pata nahi chalta post kya hai

**Solution:** Slug URL `/post/how-to-learn-python/`

**File: `blog/models.py`**
```python
# Model mein slug field
slug = models.SlugField(max_length=250)

# get_absolute_url
def get_absolute_url(self):
    return reverse('post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    # Returns: /2026/06/05/how-to-learn-python/
```

**Canonical URL Concept:**
- Agar ek post multiple URLs se accessible ho (e.g., `/post/1/` and `/post/how-to-python/`)
- Google duplicate samajh lega
- `get_absolute_url()` ek canonical (original) URL define karta hai

---

## Q3. Pagination

**Kyun chahiye?** 5000 posts ek saath load karega to page slow ho jayega

**File: `blog/views.py`**
```python
from django.core.paginator import Paginator

def post_list(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 10)   # 10 posts per page
    
    page_number = request.GET.get('page', 1)   # URL se page number lo, default 1
    posts = paginator.get_page(page_number)      # us page ki posts lo
    
    return render(request, 'blog/post_list.html', {'posts': posts})
```

**Template mein - File: `templates/blog/post_list.html`**
```html
{% if posts.has_previous %}
    <a href="?page={{ posts.previous_page_number }}">Previous</a>
{% endif %}
Page {{ posts.number }} of {{ posts.paginator.num_pages }}
{% if posts.has_next %}
    <a href="?page={{ posts.next_page_number }}">Next</a>
{% endif %}
```

---

## Q4. Class-Based Views (CBVs)

**Function View (purana tarika) - File: `blog/views.py`**
```python
def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
```

**Class-Based View (naya tarika - OOP) - File: `blog/views.py`**
```python
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Post                    # kaunsa model
    template_name = 'blog/post_list.html'   # kaunsa template
    context_object_name = 'posts'           # template mein variable ka naam
    queryset = Post.published.all()         # data kya hai
```
- Kam code likhna padta hai
- Django auto template resolve karta hai
- Inbuilt features jaise pagination easily add ho jate hain

---

## Q5. Share via Email

**File: `blog/views.py`**
```python
from django.core.mail import send_mail

def post_share(request, post_id):
    # Form se data lo
    cd = form.cleaned_data
    
    # Email bhejo
    send_mail(
        subject,           # email ka subject
        message,           # email ka body text
        'from@example.com', # sender email
        [cd['to']],         # receiver email
    )
```

**Settings mein email backend - File: `content_project/settings.py`**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # development mein console pe email print karega, actually send nahi karega
```

---

## Q6-Q8. Comment System

**Comment Model - File: `blog/models.py`**
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Ek Post ke multiple comments ho sakte hain
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']   # purane comments pehle
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
```

**Comment Form (ModelForm) - File: `blog/forms.py`**
```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']   # user se ye fields bharna hai
        # ModelForm automatically model ke fields se form bana deta hai
```

**View mein comments handle - File: `blog/views.py`**
```python
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(...)
    comments = post.comments.all()           # saare comments
    new_comment = None
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)   # abhi save mat karo
            new_comment.post = post                  # post assign karo
            new_comment.save()                       # ab save karo
```

**Template mein - File: `templates/blog/post_detail.html`**
```html
{% for comment in comments %}
    <p>{{ comment.name }}: {{ comment.body }}</p>
{% endfor %}
```

---

## Q9-Q10. Article Project (Full Practice)

**Poore project mein combine kiya:**
- Article model (title, slug, body, publish)
- Pagination
- Tagging system
- Email sharing
- Comments system

**Aapko aana chahiye:**
- Django project + app create karna
- Models define karna
- Migrations run karna (`makemigrations` → `migrate`)
- Views likhna (Function or Class-based)
- Templates banana
- URLs configure karna