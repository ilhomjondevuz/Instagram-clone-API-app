from django.urls import path

from social.views import FollowAPIView

urlpatterns = [
    path('follow/', FollowAPIView.as_view(), name='follow'),
]