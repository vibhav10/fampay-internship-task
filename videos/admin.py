from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_id', 'title', 'publishing_datetime')
    list_filter = ('user', 'publishing_datetime')
    search_fields = ('user__username', 'video_id', 'title')
    ordering = ('user', 'video_id', 'publishing_datetime')
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('user', 'video_id', 'title', 'description', 'thumbnail')}),
    )   
    add_fieldsets = (
        (None, {'fields': ('user', 'video_id', 'title', 'description', 'thumbnail')}),
    )
