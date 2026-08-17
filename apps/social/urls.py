from django.urls import path

from .views import FollowAPIView, FollowingListAPIView, FollowersListAPIView, GetOtherAPIView, HomeAPIView

urlpatterns = [
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('followings/list/', FollowingListAPIView.as_view(), name='following-list'),
    path('followers/list/', FollowersListAPIView.as_view(), name='followers-list'),
    path('user/<uuid:pk>/', GetOtherAPIView.as_view(), name='other-user'),
    path('feeds/', HomeAPIView.as_view(), name='feeds'),
]