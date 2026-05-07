from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user-profile'),
    path('<int:pk>/status/', views.update_user_status, name='user-status'),

    path('engagement/my/', views.my_engagement, name='my-engagement'),
    path('engagement/all/', views.all_student_engagement, name='all-engagement'),
    path('engagement/<int:pk>/', views.student_engagement_by_id, name='engagement-by-id'),
]
