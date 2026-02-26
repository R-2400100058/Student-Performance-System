from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count
from .models import Student, Mark, Subject
from .services import calculate_average, get_suggestions
from .forms import StudentForm, MarkForm
import json


def performance_view(request):
    students = Student.objects.all()
    return render(request, 'analytics_app/performance.html', {'students': students})


def reports_view(request):
    marks = Mark.objects.all()
    average = calculate_average(marks)
    return render(request, 'analytics_app/reports.html', {'average': average})


def suggestions_view(request):
    marks = Mark.objects.all()
    average = calculate_average(marks)
    attendance = 80  # dummy value for review-1
    suggestion = get_suggestions(average, attendance)
    return render(request, 'analytics_app/suggestions.html', {'suggestion': suggestion})


@require_http_methods(["GET"])
def get_students(request):
    """Get all students as JSON"""
    students = Student.objects.all().values('id', 'name', 'roll_no', 'department')
    return JsonResponse(list(students), safe=False)


@require_http_methods(["POST"])
def create_student(request):
    """Create a new student"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = Student.objects.create(
                name=data.get('name'),
                roll_no=data.get('roll_no'),
                department=data.get('department')
            )
            return JsonResponse({
                'success': True,
                'message': 'Student created successfully',
                'student': {
                    'id': student.id,
                    'name': student.name,
                    'roll_no': student.roll_no,
                    'department': student.department
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
def update_student(request, pk):
    """Update a student"""
    try:
        student = get_object_or_404(Student, id=pk)
        data = json.loads(request.body)
        
        student.name = data.get('name', student.name)
        student.roll_no = data.get('roll_no', student.roll_no)
        student.department = data.get('department', student.department)
        student.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Student updated successfully',
            'student': {
                'id': student.id,
                'name': student.name,
                'roll_no': student.roll_no,
                'department': student.department
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["DELETE", "POST"])
def delete_student(request, pk):
    """Delete a student"""
    try:
        student = get_object_or_404(Student, id=pk)
        student.delete()
        return JsonResponse({
            'success': True,
            'message': 'Student deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def dashboard_stats(request):
    """Get dashboard statistics"""
    total_students = Student.objects.count()
    total_marks = Mark.objects.count()
    
    avg_score = Mark.objects.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    avg_attendance = Mark.objects.aggregate(Avg('attendance_percentage'))['attendance_percentage__avg'] or 0
    
    # Calculate pass rate (assuming >= 40 is passing)
    passing_marks = Mark.objects.filter(marks_obtained__gte=40).count()
    pass_rate = (passing_marks / total_marks * 100) if total_marks > 0 else 0
    
    return JsonResponse({
        'total_students': total_students,
        'average_score': round(avg_score, 2),
        'attendance': round(avg_attendance, 2),
        'pass_rate': round(pass_rate, 2),
        'total_marks': total_marks
    })


def performance_data(request):
    """Get performance trend data for chart"""
    # Get average marks by week (for demo, we'll use marks grouped by creation)
    marks_data = Mark.objects.all().order_by('id').values_list('marks_obtained', flat=True)
    
    # Create 6 week buckets
    weeks = [[], [], [], [], [], []]
    for i, mark in enumerate(marks_data):
        week_index = i % 6
        weeks[week_index].append(mark)
    
    # Calculate average for each week
    week_averages = []
    for week in weeks:
        if week:
            avg = sum(week) / len(week)
            week_averages.append(round(avg, 2))
        else:
            week_averages.append(0)
    
    # If no data, provide sample data
    if not week_averages or all(x == 0 for x in week_averages):
        week_averages = [65, 69, 72, 75, 77, 78]
    
    return JsonResponse({
        'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
        'data': week_averages
    })


def subject_data(request):
    """Get subject comparison data for chart"""
    subjects = Subject.objects.all()
    subject_stats = []
    
    for subject in subjects:
        avg_marks = Mark.objects.filter(subject=subject).aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
        subject_stats.append({
            'name': subject.subject_name,
            'average': round(avg_marks, 2)
        })
    
    # If no data, provide sample data
    if not subject_stats:
        subject_stats = [
            {'name': 'Mathematics', 'average': 82},
            {'name': 'Science', 'average': 75},
            {'name': 'English', 'average': 88},
            {'name': 'History', 'average': 70},
            {'name': 'Geography', 'average': 79},
        ]
    
    return JsonResponse({
        'labels': [s['name'] for s in subject_stats],
        'data': [s['average'] for s in subject_stats]
    })


# ============ MARKS MANAGEMENT ENDPOINTS ============

@require_http_methods(["GET"])
def get_marks(request):
    """Get all marks as JSON"""
    marks = Mark.objects.all().select_related('student', 'subject')
    marks_data = []
    for mark in marks:
        marks_data.append({
            'id': mark.id,
            'student_id': mark.student.id,
            'student_name': mark.student.name,
            'student_roll_no': mark.student.roll_no,
            'subject_id': mark.subject.id,
            'subject_name': mark.subject.subject_name,
            'marks_obtained': mark.marks_obtained,
            'attendance_percentage': mark.attendance_percentage
        })
    return JsonResponse(marks_data, safe=False)


@require_http_methods(["POST"])
def create_mark(request):
    """Create a new mark entry"""
    try:
        data = json.loads(request.body)
        student = get_object_or_404(Student, id=data.get('student_id'))
        subject = get_object_or_404(Subject, id=data.get('subject_id'))
        
        mark = Mark.objects.create(
            student=student,
            subject=subject,
            marks_obtained=data.get('marks_obtained'),
            attendance_percentage=data.get('attendance_percentage')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Mark created successfully',
            'mark': {
                'id': mark.id,
                'student_id': mark.student.id,
                'subject_id': mark.subject.id,
                'marks_obtained': mark.marks_obtained,
                'attendance_percentage': mark.attendance_percentage
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
def update_mark(request, pk):
    """Update a mark"""
    try:
        mark = get_object_or_404(Mark, id=pk)
        data = json.loads(request.body)
        
        if 'marks_obtained' in data:
            mark.marks_obtained = data.get('marks_obtained')
        if 'attendance_percentage' in data:
            mark.attendance_percentage = data.get('attendance_percentage')
        
        mark.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Mark updated successfully',
            'mark': {
                'id': mark.id,
                'marks_obtained': mark.marks_obtained,
                'attendance_percentage': mark.attendance_percentage
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST", "DELETE"])
def delete_mark(request, pk):
    """Delete a mark"""
    try:
        mark = get_object_or_404(Mark, id=pk)
        mark.delete()
        return JsonResponse({
            'success': True,
            'message': 'Mark deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ============ SUBJECT MANAGEMENT ENDPOINTS ============

@require_http_methods(["GET"])
def get_subjects(request):
    """Get all subjects as JSON"""
    subjects = Subject.objects.all().values('id', 'subject_name')
    return JsonResponse(list(subjects), safe=False)


@require_http_methods(["POST"])
def create_subject(request):
    """Create a new subject"""
    try:
        data = json.loads(request.body)
        subject = Subject.objects.create(
            subject_name=data.get('subject_name')
        )
        return JsonResponse({
            'success': True,
            'message': 'Subject created successfully',
            'subject': {
                'id': subject.id,
                'subject_name': subject.subject_name
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)