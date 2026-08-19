from django.urls import path
from .views import SavedPostAPIView, MySavedPostListAPIView

urlpatterns = [
    path('create/', SavedPostAPIView.as_view(), name='create'),
    path('my-list/', MySavedPostListAPIView.as_view(), name='my_list'),
]