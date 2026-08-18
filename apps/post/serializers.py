from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from apps.accounts.serializers import UserSerializer
from apps.notification.models import Notification, COMMENT
from .models import Post, PostComment, CommentLike, PostLike


class PostCommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)  # body-da post_id yubormaslik uchun

    me_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = (
            'id',
            'author',
            'comment',
            'post',
            'parent',
            'created_at',
            'me_liked',
            'likes_count',
        )

    def create(self, validated_data):
        request = self.context.get('request', None)
        comment = PostComment.objects.create(**validated_data)
        # comment = super().create({
        #     **validated_data,
        #     'author': request.user,
        # })
        Notification.objects.create(
            notification_type=COMMENT,
            recipient=comment.author,
            author=request.user,
        )
        return comment

    def get_me_liked(self, obj) -> bool:
        request = self.context.get('request')

        if request:
            return obj.comment_likes.filter(
                author=request.user
            ).exists()

        return False

    def get_likes_count(self, obj) -> int:
        return obj.comment_likes.count()


class PostRetrieveAllCommentsSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    comments = PostCommentSerializer(
        many=True,
        read_only=True,
    )


class PostCommentCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = (
            'id',
            'author',
            'post',
            'comment',
            'parent',
            'created_at',
        )


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    post_likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    me_like = serializers.SerializerMethodField()
    post_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'photo',
            'caption',
            'created_at',
            'post_likes_count',
            'comments_count',
            'me_like',
            'post_comments',
        )

    def get_post_likes_count(self, obj) -> int:
        return obj.post_likes.count()

    def get_comments_count(self, obj) -> int:
        return obj.comments.count()

    def get_me_like(self, obj) -> bool:
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.post_likes.filter(
                author=request.user
            ).exists()

        return False

    def get_post_comments(self, obj) -> ReturnDict:
        """
        Postning eng so'nggi asosiy commentini qaytaradi.
        """
        comments = obj.comments.filter(
            parent=None
        ).order_by('-created_at')[:1]

        return PostCommentSerializer(
            comments,
            many=True,
            context=self.context,
        ).data


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = (
            'id',
            'author',
        )


class PostLikesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    likes_count = serializers.SerializerMethodField()
    likes = PostLikeSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'likes_count',
            'likes',
        )

    def get_likes_count(self, obj) -> int:
        return obj.post_likes.count()


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    comment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommentLike
        fields = (
            'id',
            'author',
            'comment',
        )
        read_only_fields = (
            'id',
            'author',
            'comment',
        )