from django.urls import path

from .views import FollowAPIView, FollowingListAPIView

urlpatterns = [
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('followings/list/', FollowingListAPIView.as_view(), name='following-list'),
]