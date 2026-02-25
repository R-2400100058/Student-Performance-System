from django.urls import path
from . import views

urlpatterns = [
    path('performance/', views.performance_view, name='performance'),
    path('reports/', views.reports_view, name='reports'),
    path('suggestions/', views.suggestions_view, name='suggestions'),
    
    # Student CRUD
    path('api/students/', views.get_students, name='api_students'),
    path('api/students/create/', views.create_student, name='api_create_student'),
    path('api/students/<int:pk>/update/', views.update_student, name='api_update_student'),
    path('api/students/<int:pk>/delete/', views.delete_student, name='api_delete_student'),
    
    # Dashboard data
    path('api/dashboard-stats/', views.dashboard_stats, name='api_dashboard_stats'),
    path('api/performance-data/', views.performance_data, name='api_performance_data'),
    path('api/subject-data/', views.subject_data, name='api_subject_data'),
]