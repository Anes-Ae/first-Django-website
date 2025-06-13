from django.db.models import Prefetch
from django.views import generic
from django.shortcuts import get_object_or_404, reverse


from .models import Post, Comment
from .forms import CommentForm

class HomePostListView(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.published.filter(is_featured=True)
        return context
class PostDetailView(generic.DetailView):
    template_name = 'blog/single_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        context['Related_posts'] = Post.published.filter(category=self.object.category).exclude(slug=self.object.id)[:4]
        print(context['Related_posts'])
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.published.prefetch_related(
                Prefetch(
                'comments', queryset=Comment.published.all()),
                'tags'),
            slug=self.kwargs['slug'],
        )

class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        self.post = get_object_or_404(Post, slug=self.kwargs['slug'], status=Post.POST_STATUS_PUBLISHED)
        obj.post = self.post
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('post-detail', args=[self.post.slug])
