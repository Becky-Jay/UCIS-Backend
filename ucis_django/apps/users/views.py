from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User, StudentEngagement, AlumniEngagement
from .serializers import (
    UserSerializer, UserSummarySerializer, UpdateUserSerializer,
    StudentEngagementSerializer, AlumniEngagementSerializer,
)
from .permissions import IsAdmin, IsSystemAdmin, IsStudent
from utils.audit_log import log_admin_action


class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSystemAdmin]
    serializer_class = UserSummarySerializer

    def get_queryset(self):
        return User.objects.select_related('profile').all()

    def perform_create(self, serializer):
        user = serializer.save()
        log_admin_action(
            admin=self.request.user,
            action='create_user',
            target_resource='user',
            target_id=user.id,
            details={'username': user.username, 'role': user.role},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        log_admin_action(
            admin=request.user,
            action='view_users',
            target_resource='user',
            target_id=request.user.id,
            details={'count': User.objects.count()},
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        return super().list(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsSystemAdmin]
    queryset = User.objects.select_related('profile').all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UpdateUserSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        log_admin_action(
            admin=request.user,
            action='user_deleted',
            target_resource='user',
            target_id=user.id,
            details={'username': user.username},
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            log_admin_action(
                admin=request.user,
                action='update_user',
                target_resource='user',
                target_id=kwargs['pk'],
                details=request.data,
                ip_address=request.META.get('REMOTE_ADDR'),
            )
        return response


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import UpdateProfileSerializer, UserSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return UpdateProfileSerializer
        return UserSerializer

    def get_object(self):
        return get_object_or_404(
            User.objects.select_related('profile'),
            pk=self.kwargs['pk'],
        )

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        from .serializers import UpdateProfileSerializer
        serializer = UpdateProfileSerializer(user.profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'user': UserSerializer(user).data})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdmin])
def update_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    is_active = request.data.get('is_active')
    if is_active is None:
        return Response({'message': 'is_active is required'}, status=status.HTTP_400_BAD_REQUEST)
    user.is_active = is_active
    user.save(update_fields=['is_active'])
    log_admin_action(
        admin=request.user,
        action='update_user_status',
        target_resource='user',
        target_id=user.id,
        details={'username': user.username, 'is_active': is_active},
        ip_address=request.META.get('REMOTE_ADDR'),
    )
    return Response({'message': 'User status updated', 'user': UserSummarySerializer(user).data})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def my_engagement(request):
    engagement = get_object_or_404(StudentEngagement, user=request.user)
    return Response(StudentEngagementSerializer(engagement).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def all_student_engagement(request):
    engagements = StudentEngagement.objects.select_related('user').all()
    return Response(StudentEngagementSerializer(engagements, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def student_engagement_by_id(request, pk):
    engagement = get_object_or_404(StudentEngagement, user_id=pk)
    return Response(StudentEngagementSerializer(engagement).data)
