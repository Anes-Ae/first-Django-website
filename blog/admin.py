from django.contrib import admin

from .models import *

class CommentInline(admin.TabularInline):
    model = Comment
    fields = [
        'post',
        'display_name',
        'text',
        'status',
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'post',
        'display_name',
        'status',
        'created_at',
        'updated_at',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    list_editable = [
        'status',
    ]
    list_filter = [
        'status',
        'created_at',
    ]
    list_select_related = [
        'post',
    ]


# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'description',
        'status',
        'views',
        'likes ',
        'is_featured',
        'created_at',
        'updated_at',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    list_filter = [
        'status',
    ]
    list_editable = [
        'status',
        'is_featured',
    ]
    inlines = [
        CommentInline,
    ]
