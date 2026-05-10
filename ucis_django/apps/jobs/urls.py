from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListCreateView.as_view(), name='job-list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/apply/', views.apply_for_job, name='job-apply'),
    path('<int:pk>/applications/', views.job_applications, name='job-applications'),
]
