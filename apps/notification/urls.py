from django.urls import path

from .views import MyListNotificationAPIView, MyListReadNotificationAPIView, MyListUnReadNotificationAPIView, \
    ReadNotificationAPIView, ReadingUnreadNotificationsAPIView

urlpatterns = [
    path('my-list/', MyListNotificationAPIView.as_view(), name='my-list'),
    path('my-list/read/', MyListReadNotificationAPIView.as_view(), name='my-list-read'),
    path('my-list/unread/', MyListUnReadNotificationAPIView.as_view(), name='my-list-unread'),
    path('<uuid:pk>/read/', ReadNotificationAPIView.as_view(), name='read-notification'),
    path('my-list/unread/reading/', ReadingUnreadNotificationsAPIView.as_view(), name='my-unread-list-reading'),
]