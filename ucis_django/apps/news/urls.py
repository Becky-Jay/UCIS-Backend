from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListCreateView.as_view(), name='news-list'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
]
