from googleapiclient.discovery import build
import datetime
from .models import Video
from celery import shared_task
from users.models import APIKey, SearchString
from django.db import IntegrityError

@shared_task
def get_latest_videos(max_results=15):

    # Get the latest search string for each user
    search_strings = SearchString.objects.all()
    for search_string in search_strings:
        user = search_string.user
        api_keys = list(APIKey.objects.filter(user=user).order_by('-last_used'))
        current_key_index = 0
        num_keys = len(api_keys)
        for _ in range(num_keys):
            api_key = api_keys[current_key_index].key
            try:
                search_query = search_string.search
                youtube = build('youtube', 'v3', developerKey=api_key)
                current_datetime = datetime.datetime.utcnow()
                target_datetime = current_datetime + datetime.timedelta(hours=2)
                target_datetime_str = target_datetime.isoformat() + 'Z'
                # Perform the search using the YouTube Data API
                api_keys[current_key_index].last_used = datetime.datetime.utcnow()
                api_keys[current_key_index].save()
                search_response = youtube.search().list(
                    part="id,snippet",
                    q=search_query, 
                    type='video',
                    order='date',
                    publishedAfter=target_datetime_str,
                    fields="items(id(videoId),snippet(title,description,publishedAt,thumbnails(default)))",
                    maxResults=max_results
                ).execute()

                print(search_response)
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
                    break
                except IntegrityError as e:
                    pass
                
            except Exception as e:
                pass
            current_key_index = (current_key_index + 1) % num_keys