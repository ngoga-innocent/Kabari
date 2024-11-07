from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users
from .serializer import CustomUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
class RegisterUser(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Login(APIView):
    def post(self, request, *args, **kwargs):
        identifier = request.data.get('username')  # Can be username or phone number
        password = request.data.get('password')
        
        if not identifier or not password:
            return Response(
                {'error': 'username or  phone number and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to get the user by username or phone number
        user = Users.objects.filter(username=identifier).first() or \
               Users.objects.filter(phone_number=identifier).first()

        # Authenticate user if found
        if user and user.check_password(password):
            Token.objects.filter(user=user).delete()  # Ensure a single active session
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': CustomUserSerializer(user,context={'request': request}).data
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
