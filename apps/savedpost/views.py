from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import SavedPostSerializer, SavedPostResponseSerializer


class SavedPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedPostSerializer

    @extend_schema(
        operation_id="Saved_post",
        request=SavedPostSerializer,
        responses=SavedPostResponseSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request},)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        resp_data = {
            'status': 'success',
            'message': 'Post saved successfully',
            'data': serializer.data
        }
        return Response(resp_data, status=status.HTTP_201_CREATED)