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
def teacher_marks(request):
    """Teacher marks management interface"""
    return render(request, 'accounts/teacher_marks.html')


@login_required(login_url='login')
def add_student(request):
    """Add a new student"""
    if request.method == "POST":
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        department = request.POST.get('department')

        if not name or not roll_no or not department:
            messages.error(request, "All fields are required")
            return redirect('teacher_dashboard')

        Student.objects.create(
            name=name,
            roll_no=roll_no,
            department=department
        )
        messages.success(request, f"Student {name} added successfully")
    
    return redirect('teacher_dashboard')


@login_required(login_url='login')
def delete_student(request, student_id):
    """Delete a student"""
    try:
        student = Student.objects.get(id=student_id)
        student_name = student.name
        
        # Delete associated marks
        from analytics_app.models import Mark
        Mark.objects.filter(student=student).delete()
        
        # Delete student
        student.delete()
        messages.success(request, f"Student {student_name} deleted successfully")
    except Student.DoesNotExist:
        messages.error(request, "Student not found")
    
    return redirect('teacher_dashboard')


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

    # Get detailed student data with attendance and marks
    student_data_dict = {}
    for mark in all_marks:
        student_id = mark.student.id
        if student_id not in student_data_dict:
            student_data_dict[student_id] = {
                'name': mark.student.name,
                'roll_no': mark.student.roll_no,
                'department': mark.student.department,
                'marks': [],
                'attendance': [],
            }
        student_data_dict[student_id]['marks'].append(mark.marks_obtained)
        student_data_dict[student_id]['attendance'].append(mark.attendance_percentage)

    # Build comprehensive student list
    students_list = []
    for student_id, data in student_data_dict.items():
        avg_marks = sum(data['marks']) / len(data['marks']) if data['marks'] else 0
        avg_attendance = sum(data['attendance']) / len(data['attendance']) if data['attendance'] else 0
        is_failing = avg_marks < 40  # Less than 40 is failing
        
        students_list.append({
            'id': student_id,
            'name': data['name'],
            'roll_no': data['roll_no'],
            'department': data['department'],
            'average_marks': round(avg_marks, 2),
            'attendance': round(avg_attendance, 2),
            'is_failing': is_failing,
            'total_marks_records': len(data['marks']),
        })

    # Get sorting parameter
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'marks_desc':
        students_list.sort(key=lambda x: x['average_marks'], reverse=True)
    elif sort_by == 'marks_asc':
        students_list.sort(key=lambda x: x['average_marks'])
    elif sort_by == 'attendance_desc':
        students_list.sort(key=lambda x: x['attendance'], reverse=True)
    elif sort_by == 'attendance_asc':
        students_list.sort(key=lambda x: x['attendance'])
    elif sort_by == 'failing':
        students_list.sort(key=lambda x: (not x['is_failing'], x['average_marks']))
    else:
        students_list.sort(key=lambda x: x['name'])

    # Get top students
    top_students = sorted(students_list, key=lambda x: x['average_marks'], reverse=True)[:5]

    # Get failing students
    failing_students = [s for s in students_list if s['is_failing']]

    # Overall stats
    overall_class_avg = all_marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    total_students_count = all_marks.values('student').distinct().count()
    failing_count = len(failing_students)

    context = {
        'class_stats': class_stats,
        'students_list': students_list,
        'top_students': top_students,
        'failing_students': failing_students,
        'overall_class_avg': round(overall_class_avg, 2),
        'total_students_count': total_students_count,
        'failing_count': failing_count,
        'total_marks_count': all_marks.count(),
        'sort_by': sort_by,
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
