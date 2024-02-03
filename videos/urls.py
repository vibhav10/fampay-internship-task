from django.urls import path
from . import views


urlpatterns = [
    path('videolist/', views.VideoListAPIView.as_view(), name='video-list'),
]


 