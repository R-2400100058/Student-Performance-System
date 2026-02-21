from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')

def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'accounts/teacher_dashboard.html')

def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')