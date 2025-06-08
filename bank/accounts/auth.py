from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from accounts.models import Customer
from accounts.serializers import CustomerSerializer
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import IntegrityError


class RegisterView(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                # Create a User object for authentication first
                try:
                    user = User.objects.create_user(
                        username=request.data.get('email'),
                        email=request.data.get('email'),
                        password=request.data.get('password'),
                        first_name=request.data.get('first_name'),
                        last_name=request.data.get('last_name')
                    )
                except IntegrityError:
                    return Response({'error': 'User with this email already exists'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
            
                # Add user to request data
                data = request.data.copy()
                data['user'] = user.id  # Передаем ID пользователя
                
                # Create the customer with the user reference
                serializer = CustomerSerializer(data=data)
                if serializer.is_valid():
                    customer = serializer.save()
                    
                    # Generate tokens
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name
                        },
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Please provide both email and password'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # First try to find the user by email
            user = User.objects.get(email=email)
            # Then authenticate with username (which is email) and password
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                try:
                    customer = Customer.objects.get(email=email)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'user': CustomerSerializer(customer).data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                except Customer.DoesNotExist:
                    return Response({'error': 'Customer profile not found'}, 
                                  status=status.HTTP_404_NOT_FOUND)
            return Response({'error': 'Invalid credentials'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_401_UNAUTHORIZED)