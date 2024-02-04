from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from .serializers import UserSerializer, APIKeySerializer, SearchStringSerializer
from .models import APIKey, SearchString

class TokenAuthentication(BaseTokenAuthentication):
    """
    Extend TokenAuthentication to support custom token header
    """
    keyword = 'Bearer'



'''
The UserLoginView class is an API view that handles user login functionality. 
It allows users to authenticate with their email and password, and if the credentials are valid, it returns the user's information and a token.
'''
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            return Response({
                'user': user_serializer.data,
                'token': token.key
                })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


'''
The UserCreationView class is an API view that handles the creation of a new user. It receives a POST request with user data, validates the data using the UserSerializer, 
creates a new user if the data is valid, generates a token for the user using the Token model, and returns the user data and token key in the response.
'''
class UserCreationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            return Response({
                'user': user_serializer.data,
                'token': token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

'''
The UserLogoutView class is an API view that handles user logout functionality. It requires the user to be authenticated and uses token authentication. 
When a POST request is made to this view, the user's authentication token is deleted and a response with a status code of 200 is returned.
'''
class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    



'''
The AddAPIKeyView is responsible for adding an API key for an authenticated user.
'''
class AddAPIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = APIKeySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
The RemoveAPIKeyView view allows authenticated users to remove an API key associated with their account.
'''
class RemoveAPIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user
        key_to_remove = request.data.get('key_to_remove', None)

        if key_to_remove is None:
            return Response({"error": "Please provide the 'key_to_remove' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            api_key = APIKey.objects.get(user=user, key=key_to_remove)
            api_key.delete()
            return Response({"message": "API Key removed successfully"}, status=status.HTTP_200_OK)
        except APIKey.DoesNotExist:
            return Response({"error": "API Key not found for the user"}, status=status.HTTP_404_NOT_FOUND)
        


'''
The APIKeyView view allows authenticated users to view their API keys.
'''
class APIKeyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        try:
            api_key = APIKey.objects.filter(user=user)
            serializer = APIKeySerializer(api_key, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred while fetching the API Key"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
The AddSearchStringView view allows authenticated users to add a search string to their account.
'''
class AddSearchStringView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = SearchStringSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
'''
The RemoveSearchStringView view allows authenticated users to remove a search string associated with their account.
'''
class RemoveSearchStringView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user
        try: 
            search_string = SearchString.objects.filter(user=user)
            if search_string.exists():
                search_string.delete()
                return Response({"message": "Search string removed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Search string not found for the user"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An error occurred while removing the search string"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
The SearchStringView view allows authenticated users to view their search strings.
'''
class SearchStringView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        try:
            search_string = SearchString.objects.get(user=user)
            serializer = SearchStringSerializer(search_string)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred while fetching the search string"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
