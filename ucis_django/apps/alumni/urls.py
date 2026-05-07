from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlumniProfileListView.as_view(), name='alumni-list'),
    path('me/', views.create_or_update_my_profile, name='alumni-me'),
    path('<int:pk>/', views.AlumniProfileDetailView.as_view(), name='alumni-detail'),
    path('<int:pk>/verify/', views.verify_alumni, name='alumni-verify'),
]
