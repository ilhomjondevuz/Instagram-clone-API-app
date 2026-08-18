from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class MyListNotificationAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class MyListReadNotificationAPIView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="My read notifications list",
        responses={
            200: inline_serializer(
                name='ReadNotificationsResponse',
                fields={
                    'success': serializers.BooleanField(),
                    'message': serializers.CharField(),
                    'count': serializers.IntegerField(),
                    'data': NotificationSerializer(many=True),
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        all_notifications = Notification.objects.filter(recipient=self.request.user, is_read=True)
        resp_data = {
            'success': True,
            'message': 'All read notifications',
            'count': all_notifications.count(),
            'data': self.serializer_class(all_notifications, many=True).data
        }
        return Response(data=resp_data, status=status.HTTP_200_OK)

class MyListUnReadNotificationAPIView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        all_notifications = Notification.objects.filter(recipient=self.request.user, is_read=False)
        resp_data = {
            'success': True,
            'message': 'All unread notifications',
            'count': all_notifications.count(),
            'data': self.serializer_class(all_notifications, many=True).data
        }
        return Response(data=resp_data, status=status.HTTP_200_OK)