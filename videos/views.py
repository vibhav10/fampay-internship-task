from rest_framework.views import APIView
from .models import Video
from .serializers import VideoSerializer
from .tasks import get_latest_videos
from users.models import APIKey, SearchString, User
from users.views import TokenAuthentication
from rest_framework import status, permissions
from rest_framework.response import Response

class VideoListAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        api_key = APIKey.objects.filter(user=request.user)[0].key
        search_string = SearchString.objects.get(user=request.user).search
        get_latest_videos(api_key, search_string, request.user)
        videos = Video.objects.filter(user=request.user)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

