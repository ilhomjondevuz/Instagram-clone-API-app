from django.urls import path

from .views import FollowAPIView, FollowingListAPIView, FollowersListAPIView

urlpatterns = [
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('followings/list/', FollowingListAPIView.as_view(), name='following-list'),
    path('followers/list/', FollowersListAPIView.as_view(), name='followers-list'),
]