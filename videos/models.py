from django.db import models
from users.models import User

# Create your models here.

class Video(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    publishing_datetime = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField()

    def __str__(self):
        return self.title