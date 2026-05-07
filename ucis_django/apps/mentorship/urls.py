from django.urls import path
from . import views

urlpatterns = [
    path('', views.MentorshipRequestListCreateView.as_view(), name='mentorship-list'),
    path('<int:pk>/', views.MentorshipRequestDetailView.as_view(), name='mentorship-detail'),
]
