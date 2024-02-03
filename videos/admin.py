from django.contrib import admin
from .models import Video
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_id', 'title', 'publishing_datetime')
    list_filter = ('user', 'publishing_datetime')
    search_fields = ('user', 'video_id', 'title')
    ordering = ('user', 'video_id', 'publishing_datetime')
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('user', 'video_id', 'title', 'description', 'publishing_datetime', 'thumbnail')}),
    )   
    add_fieldsets = (
        (None, {'fields': ('user', 'video_id', 'title', 'description', 'publishing_datetime', 'thumbnail')}),
    )