from django.urls import path
from .views import SavedPostAPIView

urlpatterns = [
    path('create/', SavedPostAPIView.as_view(), name='create'),
]