from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_stats, name='dashboard-stats'),
    path('student/', views.student_dashboard, name='student-dashboard'),
    path('alumni/', views.alumni_dashboard, name='alumni-dashboard'),
]
