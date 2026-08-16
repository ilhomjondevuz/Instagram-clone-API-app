from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, PostComment, PostLike, CommentLike

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author_link',
        'caption',
    )

    list_filter = (
        'author',
    )

    search_fields = (
        'caption',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    @admin.display(description='Author')
    def author_link(self, obj):
        url = reverse(
            'admin:accounts_user_change',
            args=(obj.author.pk,)
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.author.username,
        )

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_link', 'post_link', 'parent')
    list_filter = ('author', 'post')
    search_fields = ('comment', 'author__username', 'author__first_name', 'author__last_name')

    @admin.display(description='Author')
    def author_link(self, obj):
        url = reverse(
            'admin:accounts_user_change',
            args=(obj.author.pk,)
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.author.username,
        )
    @admin.display(description='Post__caption')
    def post_link(self, obj):
        url = reverse(
            'admin:post_post_change',
            args=(obj.post.pk,)
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.post.caption,
        )

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_link', 'post')
    list_filter = ('author', 'post')
    search_fields = ('author__username', 'author__first_name', 'author__last_name', 'post__caption')

    @admin.display(description='Author')
    def author_link(self, obj):
        url = reverse(
            'admin:accounts_user_change',
            args=(obj.author.pk,)
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.author.username,
        )

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_link', 'comment')
    list_filter = ('author', 'comment')
    search_fields = ('comment__comment', 'author__username', 'author__first_name', 'author__last_name')

    @admin.display(description='Author')
    def author_link(self, obj):
        url = reverse(
            'admin:accounts_user_change',
            args=(obj.author.pk,)
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.author.username,
        )