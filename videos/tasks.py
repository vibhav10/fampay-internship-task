from googleapiclient.discovery import build
import datetime 
from users.models import User  # Import your User model
from django.contrib.auth.models import User
from .models import Video  # Import your Video model

def get_latest_videos(api_key, search_query, user, max_results=3):

    youtube = build('youtube', 'v3', developerKey=api_key)

    # Get the current date and time in RFC 3339 format
    current_datetime = datetime.datetime.utcnow().isoformat() + 'Z'
    # Perform the search using the YouTube Data API
    search_response = youtube.search().list(
        part="id,snippet",
        q=search_query,
        type='video',
        order='date',
        #publishedAfter=current_datetime,
        fields="items(id(videoId),snippet(title,description,publishedAt,thumbnails(default)))",
        maxResults=max_results
    ).execute()
    videos = []
    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        publishing_datetime = item['snippet']['publishedAt']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']

        video = Video(
            user=user,
            video_id=video_id,
            title=title,
            description=description,
            publishing_datetime=publishing_datetime,
            thumbnail=thumbnail_url
        )
        videos.append(video)

    Video.objects.bulk_create(videos)