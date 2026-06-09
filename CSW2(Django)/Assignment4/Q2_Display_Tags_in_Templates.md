# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q2. Display Tags in Templates

### Step

Add the following code in the post template:

File: `blog/templates/blog/post/detail.html` or the template where a single post is displayed.

```django
<p>Tags:
{% for tag in post.tags.all %}
    <a href="{% url 'blog:post_list_by_tag' tag.slug %}">
        {{ tag.name }}
    </a>
{% endfor %}
</p>
```

### Output

```text
Tags: django | python | web
```

The tags are displayed as clickable links.
