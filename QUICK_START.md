# Quick Start Guide - Student Performance Analysis System

## 5-Minute Setup

### Step 1: Clone & Install (2 minutes)
```bash
cd c:\Users\rashm\PycharmProjects\student
git clone https://github.com/R-2400100058/Student-Performance-System.git
cd Student-Performance-System
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Database Setup (1 minute)
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Enter admin credentials when prompted
```

### Step 3: Run Server (1 minute)
```bash
python manage.py runserver
```

### Step 4: Access Application (1 minute)
- **Main URL**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Login Page**: http://localhost:8000/accounts/login

---

## First Time Usage

### 1. Create Admin Account
```
Username: admin
Password: your_secure_password
Email: admin@example.com
```

### 2. Add Sample Data
Go to Django Admin (http://localhost:8000/admin):
1. Add Students (Analytics > Students)
2. Add Subjects (Analytics > Subjects)
3. Add Terms (Analytics > Terms)
4. Add Marks (Analytics > Marks)

### 3. Test Roles
Create 3 test users:
- **Admin User**: admin / admin123
- **Teacher User**: teacher / teacher123
- **Student User**: student / student123

---

## Key URLs Reference

| Page | URL | Requires Login |
|------|-----|---|
| Home | `/` | No |
| Login | `/accounts/login/` | No |
| Sign Up | `/accounts/signup/` | No |
| Performance | `/analytics/performance/` | Yes |
| Reports | `/analytics/reports/` | Yes |
| Suggestions | `/analytics/suggestions/` | Yes |
| Admin Dashboard | `/accounts/admin-dashboard/` | Yes (Admin) |
| Teacher Dashboard | `/accounts/teacher-dashboard/` | Yes (Teacher) |
| Student Dashboard | `/accounts/student-dashboard/` | Yes (Student) |

---

## Adding Sample Data via Django Shell

### Access Django Shell
```bash
python manage.py shell
```

### Add Sample Data
```python
from analytics_app.models import Student, Subject, Term, Mark

# Create a student
student = Student.objects.create(
    name='John Doe',
    roll_no='001',
    email='john@example.com',
    class_assigned='class_10',
    department='Science'
)

# Create a subject
subject = Subject.objects.create(
    subject_name='Mathematics',
    code='MATH101',
    max_marks=100,
    passing_marks=40
)

# Create a term
term = Term.objects.create(
    term_name='term_1',
    year=2024,
    start_date='2024-01-01',
    end_date='2024-04-30'
)

# Add marks
mark = Mark.objects.create(
    student=student,
    subject=subject,
    term=term,
    marks_obtained=85,
    attendance_percentage=90
)

# Exit shell
exit()
```

---

## Features Overview

### 📊 Performance Analysis
- Real-time class analytics
- Filter by class (9-12)
- View top 10 performers
- Identify students needing support
- Score distribution charts

### 📋 Reports
- Detailed marks table
- Subject-wise filtering
- Grade tracking
- Export to CSV
- Attendance records

### 💡 Suggestions
- Personalized recommendations
- Performance analysis
- Attendance guidance
- Subject-specific tips
- Goal setting

### 📈 Student Dashboard
- Personal performance overview
- Subject scores
- Performance trends
- Grade breakdown
- Self-assessment

---

## Customization Tips

### Change Colors
Edit `templates/base_new.html`, modify CSS variables:
```css
:root {
    --primary: #4f46e5;
    --secondary: #06b6d4;
}
```

### Add More Filters
Edit `analytics_app/views.py`, add to context:
```python
context['my_filter'] = filtered_data
```

### Modify Chart Style
Edit chart options in template JavaScript:
```javascript
new Chart(ctx, {
    type: 'bar',
    options: {
        // Customize here
    }
});
```

---

## Common Commands

```bash
# Create new migration
python manage.py makemigrations app_name

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Collect static files (production)
python manage.py collectstatic

# Run tests
python manage.py test

# Create fixture for sample data
python manage.py dumpdata > fixture.json
python manage.py loaddata fixture.json
```

---

## File Structure Quick Reference

```
Key Files:
├── settings.py          ← Database & app configuration
├── urls.py              ← Main URL routing
├── requirements.txt     ← Python dependencies
├── manage.py            ← Django management
│
├── accounts/
│   ├── models.py        ← User & Profile models
│   └── views.py         ← Authentication logic
│
├── analytics_app/
│   ├── models.py        ← Student, Subject, Mark data
│   ├── services.py      ← Analytics calculations
│   ├── views.py         ← Page rendering
│   └── urls.py          ← Analytics routes
│
└── templates/
    ├── base_new.html    ← Main layout template
    ├── accounts/
    │   ├── login.html
    │   └── signup.html
    └── analytics_app/
        ├── performance.html
        ├── reports.html
        └── suggestions.html
```

---

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Database locked
**Solution**: Delete db.sqlite3 and re-migrate
```bash
rm db.sqlite3
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: Port 8000 in use
**Solution**: Use different port
```bash
python manage.py runserver 8001
```

---

## Next Steps

1. ✅ Set up development environment
2. ✅ Add sample data
3. ✅ Test login/signup
4. ✅ Explore dashboards
5. 📖 Read IMPLEMENTATION_GUIDE.md for advanced features
6. 🔧 Customize for your school
7. 📝 Add real data
8. 🚀 Deploy to production

---

## Support Resources

- **Documentation**: IMPLEMENTATION_GUIDE.md
- **Django Docs**: https://docs.djangoproject.com/
- **Chart.js**: https://www.chartjs.org/
- **Bootstrap**: https://getbootstrap.com/

---

Happy analyzing! 📊📈
