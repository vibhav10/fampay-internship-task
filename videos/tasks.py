from googleapiclient.discovery import build
import datetime 
from users.models import User  # Import your User model
from django.contrib.auth.models import User
from .models import Video  # Import your Video model
from celery import shared_task
from users.models import User, APIKey, SearchString
from django.db import IntegrityError

@shared_task
def get_latest_videos(max_results=3):

    # Get the latest search string for each user
    search_strings = SearchString.objects.all()
    for search_string in search_strings:
        user = search_string.user
        api_key = APIKey.objects.get(user=user).key
        search_query = search_string.search

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
        existing_video_ids = set(Video.objects.filter(user=user).values_list('video_id', flat=True))

        for item in search_response.get('items', []):
            video_id = item['id']['videoId']

            # Check if the video ID already exists in the database
            if video_id in existing_video_ids:
                continue  # Skip this video, it already exists

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

        try:
            Video.objects.bulk_create(videos)
        except IntegrityError as e:
            # Handle integrity error, log or raise as needed
            pass
