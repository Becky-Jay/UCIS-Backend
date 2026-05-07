from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmergencyContactListCreateView.as_view(), name='emergency-contact-list'),
    path('<int:pk>/', views.EmergencyContactDetailView.as_view(), name='emergency-contact-detail'),
]
