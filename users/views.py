from rest_framework import generics
from .serializers import UserRegisterSerializer, ResendVerificationEmailSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from django.db import transaction


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    'message': 'Registration successful! Please check your email for verification link.',
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': 'Registration failed. Please try again later.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'Invalid data provided.',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(APIView):
    """Separate API for resending verification email"""
    
    def post(self, request):
        serializer = ResendVerificationEmailSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            email_sent = serializer.send_verification_email(email, request)
            
            if email_sent:
                return Response({
                    'message': 'Verification email sent successfully!'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to send verification email. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'error': 'Invalid data provided.',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Invalid verification link'
            }, status=status.HTTP_400_BAD_REQUEST)

        if user and default_token_generator.check_token(user, token):
            if user.is_active:
                return Response({
                    'message': 'Email already verified'
                }, status=status.HTTP_200_OK)
            
            user.is_active = True
            user.save()
            return Response({
                'message': 'Email verified successfully!'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid or expired verification link'
            }, status=status.HTTP_400_BAD_REQUEST)