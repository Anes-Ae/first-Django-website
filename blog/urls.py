from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePostListView.as_view(), name='home'),
    path('posts/<str:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('comment/<str:slug>/', views.CommentCreateView.as_view(), name='comment-create'),
]
