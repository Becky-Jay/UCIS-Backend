from django.urls import path
from . import views

urlpatterns = [
    path('', views.AuditLogListView.as_view(), name='audit-log-list'),
    path('stats/', views.AuditLogStatsView.as_view(), name='audit-log-stats'),
    path('<int:pk>/', views.AuditLogDetailView.as_view(), name='audit-log-detail'),
    path('user/<int:user_id>/', views.AuditLogByUserView.as_view(), name='audit-log-by-user'),
    path('resource/<str:resource>/<str:target_id>/', views.AuditLogByResourceView.as_view(), name='audit-log-by-resource'),
]
