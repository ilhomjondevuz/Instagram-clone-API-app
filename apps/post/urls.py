from django.urls import path

from .views import PostListAPIView, PostCreateAPIView, PostRetrieveUpdateDestroyAPIView, PostCommentListAPIView, \
    PostCommentCreateAPIView, PostLikeListAPIView, PostToggleLikeAPIView, PostCommentLikeListAPIView, \
    PostCommentToggleLikeAPIView, PostCommentRetrieveAPIView, PostCommentUpdateAPIView, PostCommentDeleteAPIView, \
    PostCommentRetrieveUpdateDeleteAPIView, PostSearchAPIVIew

urlpatterns = [
    path('all/', PostListAPIView.as_view(), name='all_posts'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='detail'),

    path('<uuid:pk>/comments/', PostCommentListAPIView.as_view(), name='comments'),
    path('<uuid:pk>/comments/create/', PostCommentCreateAPIView.as_view(), name='comment-create'),
    # path('comments/<uuid:pk>/retrieve/', PostCommentRetrieveAPIView.as_view(), name='comment-retrieve'),
    # path('comments/<uuid:pk>/update/', PostCommentUpdateAPIView.as_view(), name='comment-update'),
    # path('comments/<uuid:comment_id>/delete/', PostCommentDeleteAPIView.as_view(), name='comment-delete'),
    path('comments/<uuid:comment_id>/', PostCommentRetrieveUpdateDeleteAPIView.as_view(), name='comment-detail-update-delete'),

    path('<uuid:pk>/likes/', PostLikeListAPIView.as_view(), name='likes'),  # post likes ro'yxati!
    path('<uuid:pk>/toggle-like/', PostToggleLikeAPIView.as_view(), name='toggle-like'),  # post like bosish yoki o'chirish
    path('comments/<uuid:comment_id>/likes/', PostCommentLikeListAPIView.as_view(), name='comment-likes'),  # comment likes list
    path('comments/<uuid:comment_id>/toggle-like/', PostCommentToggleLikeAPIView.as_view(), name='toggle-comment-like'),  # comment like create delete

    path('search/', PostSearchAPIVIew.as_view(), name='search'),
]