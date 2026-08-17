from django.contrib.auth import get_user_model
from django.db import models

from apps.shared.models import BaseModel


User = get_user_model()

class Follow(BaseModel):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower.username} follows -> {self.following.username}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'follower'],
                name='unique_follewer_following'
            )
        ]
        db_table = 'follows'
        ordering = ['-created_at']
        verbose_name = 'Follow '
        verbose_name_plural = 'Follows'