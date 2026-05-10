from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/react/', views.react_to_post, name='post-react'),
    path('<int:pk>/react/remove/', views.remove_reaction, name='post-unreact'),
    path('<int:pk>/comments/', views.add_comment, name='post-comment'),
    path('<int:pk>/comments/<int:comment_pk>/', views.delete_comment, name='comment-delete'),

    path('stories/', views.StoryListCreateView.as_view(), name='story-list'),
    path('stories/<int:pk>/view/', views.view_story, name='story-view'),
    path('stories/<int:pk>/', views.delete_story, name='story-delete'),
]
