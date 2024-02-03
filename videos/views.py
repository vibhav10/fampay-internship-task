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
        api_key = APIKey.objects.filter(user=request.user)[0].key
        search_string = SearchString.objects.get(user=request.user).search
        get_latest_videos(api_key, search_string, request.user)
        videos = Video.objects.filter(user=request.user)

        # Add pagination
        paginator = CustomPageNumberPagination()
        paginated_videos = paginator.paginate_queryset(videos, request)
        serializer = VideoSerializer(paginated_videos, many=True)

        return paginator.get_paginated_response(serializer.data)