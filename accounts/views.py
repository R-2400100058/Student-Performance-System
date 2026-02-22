from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  # ← ADD THIS
from .models import Profile

def home_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    return redirect('login')


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
    from django.contrib.auth.models import User
    from accounts.models import Profile
    from analytics_app.models import Mark, Attendance, Subject
    from django.db.models import Avg, Count

    # Total counts
    total_users = User.objects.count()
    total_students = Profile.objects.filter(role='Student').count()
    total_teachers = Profile.objects.filter(role='Teacher').count()
    total_subjects = Subject.objects.count()

    # Performance metrics
    total_marks = Mark.objects.count()
    avg_student_score = Mark.objects.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0

    # Recent marks
    recent_marks = Mark.objects.select_related('student', 'subject').order_by('-date')[:5]
    recent_marks_list = []
    for mark in recent_marks:
        recent_marks_list.append({
            'student': mark.student.first_name + ' ' + mark.student.last_name,
            'subject': mark.subject.name,
            'marks': mark.marks_obtained,
            'date': mark.date,
        })

    # Top performing subjects
    subject_performance = []
    for subject in Subject.objects.all():
        avg = Mark.objects.filter(subject=subject).aggregate(Avg('marks_obtained'))['marks_obtained__avg']
        if avg:
            subject_performance.append({
                'name': subject.name,
                'average': round(avg, 2),
            })
    subject_performance.sort(key=lambda x: x['average'], reverse=True)
    subject_performance = subject_performance[:5]

    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
        'total_marks': total_marks,
        'avg_student_score': round(avg_student_score, 2),
        'recent_marks': recent_marks_list,
        'subject_performance': subject_performance,
    }

    return render(request, 'accounts/admin_dashboard.html', context)


@login_required(login_url='login')
def teacher_dashboard(request):
    from analytics_app.models import Mark, Subject
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
                'name': subject.name,
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
            student_data[student_id] = {'marks': [], 'name': mark.student.first_name + ' ' + mark.student.last_name}
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
    from analytics_app.models import Mark, Attendance, Subject
    from django.db.models import Avg, Count, Q

    student = request.user

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
                'name': subject.name,
                'average': round(avg_marks, 2),
                'percentage': round((avg_marks / 100) * 100, 2),
            })

    # Calculate overall average
    overall_avg = all_marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0

    # Calculate attendance
    total_attendance = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, is_present=True).count()
    attendance_percentage = (present_days / total_attendance * 100) if total_attendance > 0 else 0

    context = {
        'subject_performance': subject_performance,
        'overall_average': round(overall_avg, 2),
        'attendance_percentage': round(attendance_percentage, 2),
        'total_marks': all_marks.count(),
    }

    return render(request, 'accounts/student_dashboard.html', context)
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')
