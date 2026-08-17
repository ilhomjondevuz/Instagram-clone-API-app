from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    follower = serializers.PrimaryKeyRelatedField(read_only=True)
    following_owner = serializers.SerializerMethodField('get_following_owner')
    follower_owner = serializers.SerializerMethodField('get_follower_owner')

    class Meta:
        model = Follow
        fields = (
            'id',
            'follower',  # qaysi foydalanuvchi follow(kuzatmoqda) bosmoqda
            'following',  # qaysi foydalanuvchi kuzatilmoqda
            'following_owner',  # kim follow bosganligi
            'follower_owner',  # kimga follow bosganligi
            'created_at',
        )
        read_only_fields = (
            'id',
            'follower',
            'created_at',
        )

    def get_following_owner(self, instance) -> UserSerializer:
        return UserSerializer(instance.follower).data

    def get_follower_owner(self, instance) -> UserSerializer:
        return UserSerializer(instance.following).data