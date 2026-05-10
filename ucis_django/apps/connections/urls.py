from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConnectionListCreateView.as_view(), name='connection-list'),
    path('<int:pk>/respond/', views.respond_to_connection, name='connection-respond'),
    path('<int:pk>/remove/', views.remove_connection, name='connection-remove'),

    path('messages/inbox/', views.inbox, name='message-inbox'),
    path('messages/<int:user_id>/', views.ConversationView.as_view(), name='conversation'),
]
