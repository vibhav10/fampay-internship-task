from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Video
from .serializers import VideoSerializer
from .tasks import get_latest_videos
from users.models import APIKey, SearchString, User
from users.views import TokenAuthentication
from rest_framework import status, permissions
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page here

class VideoListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # Get videos belonging to the authenticated user
        user_videos = Video.objects.filter(user=request.user).order_by('-publishing_datetime')

        # Paginate the videos
        paginator = CustomPageNumberPagination()
        paginated_videos = paginator.paginate_queryset(user_videos, request)
        
        # Serialize the paginated videos
        video_serializer = VideoSerializer(paginated_videos, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(video_serializer.data)