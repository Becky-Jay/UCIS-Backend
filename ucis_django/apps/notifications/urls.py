from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyNotificationsView.as_view(), name='notification-list'),
    path('<int:pk>/seen/', views.mark_seen, name='notification-seen'),
    path('mark-all-seen/', views.mark_all_seen, name='notification-all-seen'),
    path('<int:pk>/', views.delete_notification, name='notification-delete'),
]
