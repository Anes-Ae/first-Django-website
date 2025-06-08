from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePostListView.as_view(), name='home'),
]