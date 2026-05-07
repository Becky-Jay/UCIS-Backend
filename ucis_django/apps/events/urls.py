from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListCreateView.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('<int:pk>/register/', views.register_for_event, name='event-register'),
    path('<int:pk>/unregister/', views.unregister_from_event, name='event-unregister'),
]
