from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher-marks/', views.teacher_marks, name='teacher_marks'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('add-student/', views.add_student, name='add_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    
    # Include analytics URLs
    path('analytics/', include('analytics_app.urls')),
]