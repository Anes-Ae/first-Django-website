from django.views import generic
from django.shortcuts import get_object_or_404, reverse

from .models import Post, Comment
from .forms import CommentForm

class HomePostListView(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'


class PostDetailView(generic.DetailView):
    template_name = 'blog/single_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data()
        contex['comment_form'] = CommentForm
        return contex

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.prefetch_related('comments','tags'),
            slug=self.kwargs['slug'],
        )

class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        self.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        obj.post = self.post
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('post-detail', args=[self.post.slug])




