import logging
from datetime import timedelta

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from apps.users.models import User
from utils.email_service import send_email
from .serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer

logger = logging.getLogger(__name__)


def _get_tokens(user):
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.role
    return str(refresh.access_token), str(refresh)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Validation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    access, refresh = _get_tokens(user)

    return Response({
        'message': 'User registered successfully',
        'token': access,
        'refresh': refresh,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'college': user.college,
            'profile': {
                'firstName': user.profile.first_name,
                'lastName': user.profile.last_name,
            },
        },
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Validation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'message': 'Account is deactivated'}, status=status.HTTP_403_FORBIDDEN)

    user.save(update_fields=['last_active'])
    access, refresh = _get_tokens(user)

    profile = getattr(user, 'profile', None)
    return Response({
        'message': 'Login successful',
        'token': access,
        'refresh': refresh,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'college': user.college,
            'profile': {
                'firstName': profile.first_name if profile else '',
                'lastName': profile.last_name if profile else '',
                'profilePicture': profile.profile_picture if profile else '',
                'department': profile.department if profile else '',
                'mentorshipAvailability': profile.mentorship_availability if profile else False,
            } if profile else {},
        },
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    user = User.objects.filter(username=username).first()
    if not user:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    reset_token = jwt.encode(
        {'user_id': user.id},
        settings.SECRET_KEY,
        algorithm='HS256',
    )

    try:
        send_email(
            to=email,
            subject='UDSM Connect Password Reset',
            text=f'Use this token to reset your password: {reset_token}',
            html=f'<p>Use this link to reset your password:</p>'
                 f'<p><a href="http://localhost:3000/reset-password?token={reset_token}">Reset Password</a></p>',
        )
    except Exception:
        return Response({'message': 'Failed to send reset email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Password reset link sent'})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = serializer.validated_data['token']
    password = serializer.validated_data['password']

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(pk=payload['user_id'])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()

    return Response({'message': 'Password reset successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass
    return Response({'message': 'Logged out successfully'})
