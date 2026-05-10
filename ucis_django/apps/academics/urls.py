from django.urls import path
from . import views

urlpatterns = [
    path('deadlines/', views.DeadlineListCreateView.as_view(), name='deadline-list'),
    path('deadlines/<int:pk>/', views.DeadlineDetailView.as_view(), name='deadline-detail'),
    path('almanac/', views.AlmanacEventListCreateView.as_view(), name='almanac-list'),
    path('almanac/<int:pk>/', views.AlmanacEventDetailView.as_view(), name='almanac-detail'),
]
