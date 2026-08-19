from django.contrib.auth import get_user_model
from django.db import models

from apps.shared.models import BaseModel
from apps.post.models import Post


User = get_user_model()

class SavedPost(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')

    def __str__(self):
        return f"{self.user} - {self.post}"

    class Meta:
        db_table = 'saved_posts'
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post',
            )
        ]