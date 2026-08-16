from django.core.exceptions import BadRequest
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.shared.custom_pagination import CustomPagination
from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, PostCommentSerializer, PostLikeSerializer, CommentLikeSerializer


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    @extend_schema(
        operation_id="get_posts",
        summary="List all posts",
        request=None,
        responses={
            200: PostSerializer,
            400: BadRequest,
        }
    )
    def get_queryset(self):
        return Post.objects.all()

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp_data = {
            "success": True,
            "data": serializer.data,
            "message": f"Post {post.caption} has been updated successfully"
        }
        return Response(resp_data, status=status.HTTP_200_OK)

class PostCommentListAPIView(generics.ListAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset

class PostCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)

class PostLikeListAPIView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostLike.objects.filter(post__id=post_id)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)

class PostToggleLikeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostLikeSerializer

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']

        post = generics.get_object_or_404(
            Post,
            pk=post_id,
        )
        like = PostLike.objects.filter(post=post, author=self.request.user).first()
        if like:
            like.delete()
            return Response({
                "success": True,
                "message": f"Post {post.caption} has been Post unliked.",
                'liked': False,
            }, status=status.HTTP_200_OK)
        PostLike.objects.create(post=post, author=self.request.user)
        return Response({
            "success": True,
            "message": f"Post {post.caption} has been Post liked.",
            'liked': True,
        })

class PostCommentLikeListAPIView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        queryset = CommentLike.objects.filter(comment__id=comment_id)
        return queryset

class PostCommentToggleLikeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentLikeSerializer

    def post(self, request, *args, **kwargs):
        comment_id = self.kwargs['comment_id']

        # MUHIM: bu yerda PostComment olinadi
        comment = get_object_or_404(
            PostComment,
            id=comment_id
        )

        # MUHIM: comment ga PostComment instance beriladi
        like = CommentLike.objects.filter(
            comment=comment,
            author=request.user
        ).first()

        if like:
            like.delete()

            return Response(
                {
                    'success': True,
                    'message': 'Comment has been unliked.',
                    'liked': False,
                },
                status=status.HTTP_200_OK
            )

        like = CommentLike.objects.create(
            comment=comment,
            author=request.user
        )

        return Response(
            {
                'success': True,
                'message': 'Comment has been liked.',
                'liked': True,
                'like': CommentLikeSerializer(
                    like,
                    context={'request': request}
                ).data,
            },
            status=status.HTTP_201_CREATED
        )

class PostCommentRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = PostComment.objects.filter(pk=pk)
        return queryset

class PostCommentUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()
    @extend_schema(
        operation_id="Comment update API",
    )
    def perform_update(self, serializer):
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(PostComment, pk=comment_id)
        if comment.author == self.request.user:
            serializer = self.serializer_class(instance=comment, data=self.request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'success': True,
                'message': 'Comment has been updated.',
                'comment': serializer.data,
            })
        return Response({
            'success': False,
            'message': 'Comment not updated.',
            'comment': "User not authorized to update comment.",
        })

class PostCommentDeleteAPIView(generics.DestroyAPIView):  # xatolik bor
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCommentSerializer
    queryset = PostComment.objects.all()

    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(PostComment, pk=comment_id, author=self.request.user)
        comment.delete()
        return Response({
            "success": True,
            "message": "Comment has been deleted.",
        })