from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from analytics_app.models import Student

def home_view(request):
    """Render landing page"""
    return render(request, 'landing.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # Save extra data in Profile model
        Profile.objects.create(
            user=user,
            gender=gender,
            role=role
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'accounts/signup.html')


# ← ADD @login_required TO THESE THREE
@login_required(login_url='login')
def admin_dashboard(request):
    """Display admin dashboard with analytics"""
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def manage_students(request):
    """Manage students CRUD interface"""
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'manage_students.html', context)


@login_required(login_url='login')
def teacher_dashboard(request):
    from analytics_app.models import Mark, Subject, Student
    from django.db.models import Avg, Count

    # Get all marks (not filtered by teacher for now)
    all_marks = Mark.objects.all()

    # Calculate class performance
    class_stats = []
    for subject in Subject.objects.all():
        subject_marks = all_marks.filter(subject=subject)
        if subject_marks.exists():
            avg = subject_marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg']
            total_students = subject_marks.values('student').distinct().count()
            class_stats.append({
                'name': subject.subject_name,
                'average': round(avg, 2),
                'total_students': total_students,
                'total_marks': subject_marks.count(),
            })

    # Get top students
    top_students = []
    student_data = {}
    for mark in all_marks:
        student_id = mark.student.id
        if student_id not in student_data:
            student_data[student_id] = {'marks': [], 'name': mark.student.name}
        student_data[student_id]['marks'].append(mark.marks_obtained)

    for student_id, data in student_data.items():
        avg = sum(data['marks']) / len(data['marks'])
        top_students.append({'name': data['name'], 'average': round(avg, 2)})

    top_students.sort(key=lambda x: x['average'], reverse=True)
    top_students = top_students[:5]

    # Overall stats
    overall_class_avg = all_marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    total_students_count = all_marks.values('student').distinct().count()

    context = {
        'class_stats': class_stats,
        'top_students': top_students,
        'overall_class_avg': round(overall_class_avg, 2),
        'total_students_count': total_students_count,
        'total_marks_count': all_marks.count(),
    }

    return render(request, 'accounts/teacher_dashboard.html', context)

@login_required(login_url='login')
def student_dashboard(request):
    from analytics_app.models import Mark, Subject, Student
    from django.db.models import Avg, Count

    # Get the student record for this user
    try:
        student = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        # If no student record exists for this user, show empty dashboard
        student = None

    if student:
        # Get all marks for this student
        all_marks = Mark.objects.filter(student=student)

        # Calculate subject-wise performance
        subject_performance = []
        subjects = Subject.objects.all()

        for subject in subjects:
            subject_marks = all_marks.filter(subject=subject)
            if subject_marks.exists():
                avg_marks = subject_marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg']
                subject_performance.append({
                    'name': subject.subject_name,
                    'average': round(avg_marks, 2),
                    'percentage': round((avg_marks / 100) * 100, 2),
                })

        # Calculate overall average
        overall_avg = all_marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0

        # Calculate attendance from average attendance_percentage
        attendance_marks = all_marks.aggregate(Avg('attendance_percentage'))['attendance_percentage__avg'] or 0

        context = {
            'subject_performance': subject_performance,
            'overall_average': round(overall_avg, 2),
            'attendance_percentage': round(attendance_marks, 2),
            'total_marks': all_marks.count(),
            'student_name': student.name,
        }
    else:
        context = {
            'subject_performance': [],
            'overall_average': 0,
            'attendance_percentage': 0,
            'total_marks': 0,
            'student_name': 'No student record found',
        }

    return render(request, 'accounts/student_dashboard.html', context)
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')
