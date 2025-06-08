from django.views import generic
from django.shortcuts import get_object_or_404

from .models import Post

class HomePostListView(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'


class PostDetailView(generic.DetailView):
    template_name = 'blog/single_post.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.prefetch_related('comments','tags'),
            slug=self.kwargs['slug'],
        )