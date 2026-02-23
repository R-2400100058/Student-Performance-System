from django.shortcuts import render
from .models import Student, Mark
from .services import calculate_average, get_suggestions


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