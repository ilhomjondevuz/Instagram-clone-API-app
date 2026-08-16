from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, FileExtensionValidator
from django.db import models

from apps.shared.models import BaseModel


User = get_user_model()

class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    photo = models.ImageField(upload_to='posts/%Y/%m', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], null=False, blank=False)
    caption = models.TextField(validators=[MaxLengthValidator(2000)], null=True, blank=True)

    def __str__(self):
        return self.caption

    class Meta:
        db_table = 'posts'
        ordering = ['-pk']
        verbose_name = 'Post '
        verbose_name_plural = 'Posts'

class PostComment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(validators=[MaxLengthValidator(500)], null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'post_comments'
        ordering = ['-pk']
        verbose_name = 'Post Comment '
        verbose_name_plural = 'Post Comments'

class PostLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return f"{self.author} - {self.post}"

    class Meta:
        db_table = 'post_likes'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'post'],
                name='unique_author_post_likes',
            )

        ]
        ordering = ['-pk']
        verbose_name = 'Post Like '
        verbose_name_plural = 'Post Likes'

class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='comment_likes')

    def __str__(self):
        return f"{self.author} - {self.comment}"

    class Meta:
        db_table = 'comment_likes'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'comment'],
                name='unique_author_comment_likes',
            )
        ]
        ordering = ['-pk']
        verbose_name = 'Comment Like '
        verbose_name_plural = 'Comment Likes'