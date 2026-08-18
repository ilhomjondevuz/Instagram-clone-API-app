from django.urls import path

from .views import MyListNotificationAPIView

urlpatterns = [
    path('my-list/', MyListNotificationAPIView.as_view(), name='all'),
]