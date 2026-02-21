from django.urls import path
from . import views

urlpatterns = [
    path('performance/', views.performance_view, name='performance'),
    path('reports/', views.reports_view, name='reports'),
    path('suggestions/', views.suggestions_view, name='suggestions'),
]