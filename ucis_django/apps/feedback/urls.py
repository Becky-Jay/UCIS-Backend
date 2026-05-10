from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeedbackListCreateView.as_view(), name='feedback-list'),
    path('<int:pk>/respond/', views.respond_to_feedback, name='feedback-respond'),
]
