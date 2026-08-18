from django.urls import path

from .views import MyListNotificationAPIView, MyListReadNotificationAPIView, MyListUnReadNotificationAPIView

urlpatterns = [
    path('my-list/', MyListNotificationAPIView.as_view(), name='my-list'),
    path('my-list/read/', MyListReadNotificationAPIView.as_view(), name='my-list-read'),
    path('my-list/unread/', MyListUnReadNotificationAPIView.as_view(), name='my-list-unread'),
]