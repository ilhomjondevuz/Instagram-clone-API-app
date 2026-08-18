from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.notification.models import Notification
from apps.post.serializers import PostSerializer, PostCommentSerializer


class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    recipient = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    comment = PostCommentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'recipient',
            'author',
            'post',
            'comment',
            'is_read',
            'created_at'
        ]

    def update(self, instance, validated_data):
        if instance.is_read:
            instance.is_read = False
        else:
            instance.is_read = True
        instance.save()
        return instance