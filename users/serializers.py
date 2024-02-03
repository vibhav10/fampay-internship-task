from rest_framework import serializers
from .models import User, APIKey, SearchString

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'

class SearchStringSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SearchString
        fields = '__all__'