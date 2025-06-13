from django.db import models
from django.utils.text import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from tinymce.models import HTMLField
from tags.models import Tag


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='pub').order_by('-created_at')

class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='pub').order_by('-created_at')

class Post(models.Model):
    POST_STATUS_PUBLISHED = 'pub'
    POST_STATUS_DRAFT = 'drf'

    POST_STATUS_CHOICES = (
        (POST_STATUS_PUBLISHED, 'published'),
        (POST_STATUS_DRAFT, 'draft'),
    )

    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), unique=True, blank=True, allow_unicode=True, help_text=_(
        'It is preferable to leave this field blank so that it will be filled in automatically.'
    ))
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='posts', verbose_name=_('author'))
    featured_image = models.ImageField(_('featured image'), upload_to='blog_images/', null=True, blank=True)
    main_content = HTMLField(_('main content'))
    reading_time = models.PositiveIntegerField(_('reading_time'), blank=True, null=True, help_text=_('In minutes'))
    description = models.TextField()
    status = models.CharField(_('status'), max_length=3, choices=POST_STATUS_CHOICES, default=POST_STATUS_DRAFT)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE,  related_name='posts', verbose_name=_('categories'))
    tags = models.ManyToManyField(Tag, related_name='posts')
    views = models.PositiveIntegerField(_('views'), default=0)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_posts', verbose_name=_('likes'))
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'title: {self.title} author: {self.author}'

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])

    @property
    def total_likes(self):
        self.likes.count()


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.replace(' ', '-')
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('blog posts')

    objects = models.Manager()
    published = PostManager()


class Comment(models.Model):
    COMMENT_STATUS_PUBLISHED = 'pub'
    COMMENT_STATUS_DRAFT = 'drf'
    COMMENT_STATUS_REJECTED = 'rjt'

    COMMENT_STATUS_CHOICES = (
        (COMMENT_STATUS_PUBLISHED, 'published'),
        (COMMENT_STATUS_DRAFT, 'draft'),
        (COMMENT_STATUS_REJECTED, 'rejected'),
    )

    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='comments', verbose_name=_('post'))
    display_name = models.CharField(_('display name'), max_length=100)
    text = models.TextField(_('text'))
    status = models.CharField(
                             _('status'),
                              max_length=3,
                              choices=COMMENT_STATUS_CHOICES,
                              default=COMMENT_STATUS_DRAFT)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    objects = models.Manager()
    published = CommentManager()