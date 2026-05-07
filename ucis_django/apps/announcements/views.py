from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdmin
from utils.audit_log import log_admin_action
from utils.notification_service import notify_announcement, notify_admin_action
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        base_qs = Announcement.objects.filter(expires_at__gt=timezone.now())

        if user.role == 'system_admin':
            return base_qs.select_related('created_by')

        if user.role == 'college_admin':
            return base_qs.filter(
                college__contains=user.college
            ).select_related('created_by')

        return base_qs.filter(
            target_roles__contains=user.role,
            college__contains=user.college,
        ).select_related('created_by')

    def perform_create(self, serializer):
        announcement = serializer.save(created_by=self.request.user)
        log_id = log_admin_action(
            admin=self.request.user,
            action='announcement_created',
            target_resource='announcement',
            target_id=announcement.id,
            details={'title': announcement.title, 'college': announcement.college},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        notify_announcement(announcement)
        notify_admin_action(
            college=announcement.college,
            message=f'Announcement "{announcement.title}" created',
            action_type='Announcement Creation',
            log_id=log_id.id if log_id else None,
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Announcements fetched successfully', 'announcements': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Announcement created successfully', 'announcement': response.data}, status=status.HTTP_201_CREATED)


class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.select_related('created_by').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def perform_update(self, serializer):
        announcement = serializer.save()
        log_id = log_admin_action(
            admin=self.request.user,
            action='announcement_updated',
            target_resource='announcement',
            target_id=announcement.id,
            details={'title': announcement.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        notify_admin_action(
            college=announcement.college,
            message=f'Announcement "{announcement.title}" updated',
            action_type='Announcement Update',
            log_id=log_id.id if log_id else None,
        )

    def perform_destroy(self, instance):
        log_id = log_admin_action(
            admin=self.request.user,
            action='announcement_deleted',
            target_resource='announcement',
            target_id=instance.id,
            details={'title': instance.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        notify_admin_action(
            college=instance.college,
            message=f'Announcement "{instance.title}" deleted',
            action_type='Announcement Deletion',
            log_id=log_id.id if log_id else None,
        )
        instance.delete()
