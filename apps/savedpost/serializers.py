from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.post.models import Post
from .models import SavedPost


class SavedPostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = SavedPost
        fields = ('id', 'post', 'user', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class SavedPostResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = SavedPostSerializer()