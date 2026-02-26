# Troubleshooting & FAQ Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Runtime Errors](#runtime-errors)
3. [Database Issues](#database-issues)
4. [Display Problems](#display-problems)
5. [Performance Issues](#performance-issues)
6. [Authentication Problems](#authentication-problems)
7. [Data Issues](#data-issues)
8. [FAQ](#faq)

---

## Installation Issues

### Issue: `No module named 'django'`
**Cause**: Django not installed or virtual environment not activated

**Solution**:
```bash
# Activate virtual environment
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import django; print(django.get_version())"
```

---

### Issue: `pip install` fails with "permission denied"
**Cause**: Permission issue with pip

**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Issue: `requirements.txt` not found
**Cause**: Wrong directory or file missing

**Solution**:
```bash
# Navigate to correct directory
cd Student-Performance-System

# Verify file exists
dir requirements.txt  # Windows
ls requirements.txt   # Mac/Linux

# If missing, recreate from pip freeze
pip freeze > requirements.txt
```

---

## Runtime Errors

### Issue: `ModuleNotFoundError: No module named '_sqlite3'`
**Cause**: Python SQLite module not installed

**Solution (Windows)**:
```bash
# Reinstall Python with SQLite
# Download Python installer from python.org
# Run installer, check "tcl/tk and IDLE" and "pip"
```

**Solution (Mac/Linux)**:
```bash
# Debian/Ubuntu
sudo apt-get install python3-tk python3-dev

# Or reinstall Python with SQLite support
```

---

### Issue: `TemplateDoesNotExist: base_new.html`
**Cause**: Template file not found or TEMPLATES setting incorrect

**Solution**:
```python
# Check TEMPLATES in settings.py
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],  # Verify path
        'APP_DIRS': True,  # Must be True
    }
]

# Check file exists
# File should be at: Student-Performance-System/templates/base_new.html
```

---

### Issue: `ModuleNotFoundError: No module named 'analytics_app'`
**Cause**: App not in INSTALLED_APPS

**Solution**:
```python
# Edit settings.py
INSTALLED_APPS = [
    # ...
    'accounts',
    'analytics_app',  # Add this
]
```

---

## Database Issues

### Issue: `ProgrammingError: relation "analytics_app_student" does not exist`
**Cause**: Migrations not applied

**Solution**:
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Verify
python manage.py migrate --list
```

---

### Issue: `sqlite3.IntegrityError: UNIQUE constraint failed`
**Cause**: Duplicate entry in unique field

**Solution**:
```bash
# Delete database and start fresh
rm db.sqlite3  # Windows: del db.sqlite3

# Re-migrate
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

---

### Issue: Database locked
**Cause**: Database in use or corrupt

**Solution**:
```bash
# Method 1: Delete and recreate
rm db.sqlite3
python manage.py migrate

# Method 2: Check Django connections
python manage.py dbshell
.quit

# Method 3: Restart development server
# Stop: Ctrl+C
# Start: python manage.py runserver
```

---

### Issue: `ProgrammingError` when accessing admin
**Cause**: Missing migrations after model changes

**Solution**:
```bash
# Check model changes
python manage.py makemigrations --dry-run

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

---

## Display Problems

### Issue: Styling broken (no colors/layout)
**Cause**: CSS not loaded or static files not served

**Solution**:
```python
# In settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Collect static files
python manage.py collectstatic --noinput
```

**For Development**:
```python
# Add to settings.py
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

### Issue: Charts not displaying (blank chart area)
**Cause**: Chart.js not loaded or data incorrect

**Solution**:
1. Check browser console (F12 → Console tab)
2. Verify Chart.js CDN is accessible
3. Check data format in template:
```django
{% if pass_fail_data %}
    {{pass_fail_data|safe}}  {# Verify this displays correctly #}
{% endif %}
```
4. Try different data structure

---

### Issue: Images/Icons not showing
**Cause**: Font Awesome CDN not loaded or offline

**Solution**:
```html
<!-- Verify in base_new.html -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- If offline, use icon alternatives -->
<i class="fas fa-chart-line"></i>  <!-- Instead use -->
<span>📊</span>  <!-- Alternative -->
```

---

### Issue: Navbar looks broken on mobile
**Cause**: Bootstrap not loaded or responsive CSS issue

**Solution**:
```html
<!-- Verify in base_new.html -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Check viewport meta tag -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

---

## Performance Issues

### Issue: Page loads slowly
**Cause**: Large data queries or missing indexes

**Solution**:
```python
# In views.py, use select_related for foreign keys
from django.db.models import prefetch_related

marks = Mark.objects.select_related(
    'student', 'subject', 'term'
).all()

# Add database indexes
# In models.py
class Meta:
    indexes = [
        models.Index(fields=['student', 'term']),
        models.Index(fields=['subject', 'term']),
    ]
```

---

### Issue: Charts take long time to render
**Cause**: Large dataset or complex calculations

**Solution**:
```python
# Limit data in view
def performance_view(request):
    # Only get necessary fields
    marks = Mark.objects.filter(
        student__class_assigned=class_filter
    ).values('marks_obtained')[:1000]  # Limit to 1000
    
    # Pre-calculate in backend
    avg_score = sum(m['marks_obtained'] for m in marks) / len(marks)
```

---

### Issue: Database queries too many
**Cause**: N+1 query problem

**Solution**:
```python
# Instead of:
for mark in marks:
    print(mark.student.name)  # Separate query each time

# Use:
marks = marks.select_related('student', 'subject')
for mark in marks:
    print(mark.student.name)  # Already fetched
```

---

## Authentication Problems

### Issue: Login page loops back to login
**Cause**: Incorrect redirect URL or role mismatch

**Solution**:
```python
# Check in accounts/views.py
def login_view(request):
    if user is not None:
        login(request, user)
        
        # Verify role matches what's in database
        if role == 'admin':
            return redirect('admin_dashboard')
        # etc.

# Check in settings.py
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'  # or your default URL
```

---

### Issue: "Permission denied" accessing admin pages
**Cause**: User not logged in or wrong role

**Solution**:
```python
# Use login_required decorator
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    return render(request, 'template.html')

# Or check role
def admin_only(request):
    if not request.user.profile.role == 'admin':
        return redirect('home')
    return render(request, 'admin.html')
```

---

### Issue: Cannot create superuser
**Cause**: Already exists or input error

**Solution**:
```bash
# Check if superuser exists
python manage.py shell
from django.contrib.auth.models import User
User.objects.filter(is_superuser=True)
exit()

# Delete and recreate
python manage.py shell
from django.contrib.auth.models import User
User.objects.filter(username='admin').delete()
exit()

# Create new superuser
python manage.py createsuperuser
```

---

### Issue: "Incorrect username or password"
**Cause**: Wrong credentials or encoding issue

**Solution**:
```python
# Test in shell
python manage.py shell
from django.contrib.auth import authenticate
user = authenticate(username='test', password='test123')
print(user)  # Should print user object or None
exit()

# If None, password may be incorrect
# Reset password
python manage.py changepassword username
```

---

## Data Issues

### Issue: No data appearing in analytics
**Cause**: No marks created or filter too restrictive

**Solution**:
```python
# Add sample data via Django shell
python manage.py shell

from analytics_app.models import Student, Subject, Term, Mark

# Create if not exists
student, _ = Student.objects.get_or_create(
    roll_no='001',
    defaults={'name': 'Test Student', 'class_assigned': 'class_10'}
)

subject, _ = Subject.objects.get_or_create(
    code='MATH',
    defaults={'subject_name': 'Mathematics'}
)

term, _ = Term.objects.get_or_create(
    term_name='term_1',
    year=2024,
    defaults={'start_date': '2024-01-01', 'end_date': '2024-04-30'}
)

Mark.objects.create(student=student, subject=subject, term=term, 
                    marks_obtained=85, attendance_percentage=90)

exit()
```

---

### Issue: Grades not calculated
**Cause**: Mark.save() not called or grade field not saved

**Solution**:
```python
# Force recalculation
python manage.py shell
from analytics_app.models import Mark

for mark in Mark.objects.all():
    mark.save()  # Triggers grade calculation

exit()
```

---

### Issue: Filters not working
**Cause**: Wrong query parameter or field name

**Solution**:
```python
# Check in views.py
def performance_view(request):
    class_filter = request.GET.get('class')  # URL param name
    
    # Verify field exists in model
    marks = Mark.objects.filter(
        student__class_assigned=class_filter  # Must match model field
    )
```

---

## FAQ

### Q: Can I use PostgreSQL instead of SQLite?
**A**: Yes. In settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'student_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### Q: How do I backup my database?
**A**: 
```bash
# Create fixture (backup)
python manage.py dumpdata > backup.json

# Restore from fixture
python manage.py loaddata backup.json

# Copy SQLite file
cp db.sqlite3 db.sqlite3.backup
```

---

### Q: How do I reset to factory defaults?
**A**:
```bash
# Delete database
rm db.sqlite3

# Re-migrate
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

---

### Q: Can I change the port number?
**A**: Yes:
```bash
# Use different port
python manage.py runserver 8001

# Or
python manage.py runserver 0.0.0.0:9000
```

---

### Q: How do I enable HTTPS?
**A**: 
```python
# In settings.py for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

### Q: Can I add more users?
**A**: Yes, via signup page or admin:
```bash
# Via shell
python manage.py createsuperuser  # Admin
python manage.py shell
from django.contrib.auth.models import User
User.objects.create_user(username='teacher1', password='pass123')
exit()
```

---

### Q: How do I modify the grade scale?
**A**: Edit in analytics_app/models.py:
```python
def save(self):
    if self.marks_obtained >= 95:  # Change these thresholds
        self.grade = 'A+'
    # ... modify as needed
```

---

### Q: How do I export all data?
**A**:
```bash
# Export to JSON
python manage.py dumpdata > all_data.json

# Export to CSV (from Reports page)
# Click "Export CSV" button (if implemented)
```

---

### Q: Can I run this on a server?
**A**: Yes, use production setup:
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn student_performance_system.wsgi:application

# Use nginx as reverse proxy (see Django docs)
```

---

### Q: How do I send emails?
**A**: Configure email backend:
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

---

### Q: Can I use this with Docker?
**A**: Yes, create Dockerfile:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

### Q: How do I deploy to Heroku?
**A**: 
```bash
# Install Heroku CLI
# Create Procfile:
web: gunicorn student_performance_system.wsgi

# Create runtime.txt:
python-3.11.0

# Deploy
heroku login
heroku create app-name
git push heroku main
heroku run python manage.py migrate
```

---

### Q: Can I customize the dashboard?
**A**: Yes, edit templates in:
```
templates/accounts/admin_dashboard.html
templates/accounts/teacher_dashboard.html
templates/accounts/student_dashboard.html
```

---

### Q: How do I add a new field?
**A**:
```python
# 1. Add to model
class Student(models.Model):
    new_field = models.CharField(max_length=100)

# 2. Create migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate

# 4. Update forms and templates
```

---

### Q: Performance is slow with many students
**A**: 
1. Add database indexes (see Performance Issues)
2. Use pagination on tables
3. Cache aggregated data
4. Optimize queries with select_related

---

## Getting More Help

- **Django Documentation**: https://docs.djangoproject.com
- **Stack Overflow**: Tag with `django`
- **GitHub Issues**: Report bugs
- **Community Forums**: Django discussion board

---

**Last Updated**: February 2026
