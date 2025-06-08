from django.shortcuts import render
from django.views import generic

from .models import Post

class HomePostListView(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'