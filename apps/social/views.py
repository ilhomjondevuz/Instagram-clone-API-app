from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.notification.models import Notification, FOLLOW, UN_FOLLOW
from .models import Follow
from .serializers import FollowSerializer


class FollowAPIView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        follower = request.user
        following = serializer.validated_data['following']

        follow = Follow.objects.filter(
            follower=follower,
            following=following
        ).first()

        if follow:
            follow.delete()

            Notification.objects.create(
                recipient=following,
                author=follower,
                notification_type=UN_FOLLOW,
            )

            return Response({
                'success': True,
                'message': 'Unfollow successful.',
                'is_following': False,
            })

        Follow.objects.create(
            follower=follower,
            following=following,
        )

        Notification.objects.create(
            recipient=following,
            author=follower,
            notification_type=FOLLOW,
        )

        return Response({
            'success': True,
            'message': 'Follow successful.',
            'is_following': True,
        }, status=status.HTTP_201_CREATED)