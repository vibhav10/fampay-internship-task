from django.urls import path
from . import views


urlpatterns = [
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/register/', views.UserCreationView.as_view(), name='register'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('apikeys/', views.APIKeyView.as_view(), name='apikey'),
    path('addapikey/', views.AddAPIKeyView.as_view(), name='addapikey'),
    path('removeapikey/', views.RemoveAPIKeyView.as_view(), name='removeapikey'),
    path('searchstring/', views.SearchStringView.as_view(), name='searchstring'),
    path('addsearchstring/', views.AddSearchStringView.as_view(), name='addsearchstring'),
    path('removesearchstring/', views.RemoveSearchStringView.as_view(), name='removesearchstring'),
]


 