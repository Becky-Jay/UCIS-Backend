from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='auth-register'),
    path('login/', views.login, name='auth-login'),
    path('logout/', views.logout, name='auth-logout'),
    path('me/', views.me, name='auth-me'),
    path('change-password/', views.change_password, name='auth-change-password'),
    path('token/refresh/', views.token_refresh, name='auth-token-refresh'),
    path('forgot-password/', views.forgot_password, name='auth-forgot-password'),
    path('reset-password/', views.reset_password, name='auth-reset-password'),
]
