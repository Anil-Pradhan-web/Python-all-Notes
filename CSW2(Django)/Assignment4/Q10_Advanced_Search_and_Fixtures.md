# Assignment 4 - Extending Your Blog Application

Course: CSW-2 (CSE 3141)  
Semester: 4th

---

## Q10. Advanced Search + Fixtures

### Step 1: Dump Data

Export project data into a JSON fixture:

Command location: Run this command from the folder that contains `manage.py`.

```bash
python manage.py dumpdata > data.json
```

### Step 2: Load Data

Import data from the fixture:

Command location: Run this command from the folder that contains `manage.py`.

```bash
python manage.py loaddata data.json
```

### Step 3: Search

Search posts by title:

File: `blog/views.py` or Django shell for testing.

```python
Post.objects.filter(title__icontains='django')
```

### Output

- Data is exported successfully.
- Data is imported successfully.
- Search works efficiently.
