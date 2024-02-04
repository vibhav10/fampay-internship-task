from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address") 
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user    
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not email:
            raise ValueError("Users must have an email address")   
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
    
class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    


class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + " " + self.key
    

class SearchString(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    search = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user) + " " + self.search