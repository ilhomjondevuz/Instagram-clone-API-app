from rest_framework import serializers

from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    follower = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = (
            'id',
            'follower',
            'following',
            'created_at',
        )
        read_only_fields = (
            'id',
            'follower',
            'created_at',
        )