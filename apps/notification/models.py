from django.contrib.auth import get_user_model
from django.db import models

from apps.shared.models import BaseModel
from apps.post.models import Post, PostComment

FOLLOW, UN_FOLLOW, LIKE, COMMENT, COMMENT_LIKE = 'follow', 'un_follow', 'like', 'comment', 'comment_like'
NOTIFICATION_TYPES = (
    (FOLLOW, FOLLOW),
    (UN_FOLLOW, UN_FOLLOW),
    (LIKE, LIKE),
    (COMMENT, COMMENT_LIKE),
    (COMMENT_LIKE, COMMENT_LIKE),
)

User = get_user_model()

class Notification(BaseModel):
    notification_type = models.CharField(max_length=12, choices=NOTIFICATION_TYPES)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.notification_type}: {self.recipient} -> {self.author}"

    class Meta:
        db_table = 'notification'
        ordering = ['-created_at']
        verbose_name = 'Notification '
        verbose_name_plural = 'Notifications'