from django.urls import path
from . import views


urlpatterns = [
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/register/', views.UserCreationView.as_view(), name='register'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
]


 