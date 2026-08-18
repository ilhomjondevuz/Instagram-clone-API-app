from django.urls import path

from .views import MyListNotificationAPIView, MyListReadNotificationAPIView

urlpatterns = [
    path('my-list/', MyListNotificationAPIView.as_view(), name='my-list'),
    path('my-list/read/', MyListReadNotificationAPIView.as_view(), name='my-list-read'),
]