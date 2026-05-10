from django.urls import path
from . import views

urlpatterns = [
    path('', views.CampusLocationListCreateView.as_view(), name='campus-list'),
    path('<int:pk>/', views.CampusLocationDetailView.as_view(), name='campus-detail'),
]
