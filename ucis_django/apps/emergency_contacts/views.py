from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdmin
from utils.audit_log import log_admin_action
from .models import EmergencyContact
from .serializers import EmergencyContactSerializer


class EmergencyContactListCreateView(generics.ListCreateAPIView):
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = EmergencyContact.objects.all()
        if user.role not in ('system_admin', 'college_admin'):
            qs = qs.filter(visible_to__contains=user.role)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        contact = serializer.save()
        log_admin_action(
            admin=self.request.user,
            action='emergency_contact_created',
            target_resource='emergency_contact',
            target_id=contact.id,
            details={'name': contact.name, 'category': contact.category},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Emergency contacts fetched', 'contacts': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Emergency contact created', 'contact': response.data}, status=status.HTTP_201_CREATED)


class EmergencyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmergencyContactSerializer
    queryset = EmergencyContact.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def perform_update(self, serializer):
        contact = serializer.save()
        log_admin_action(
            admin=self.request.user,
            action='emergency_contact_updated',
            target_resource='emergency_contact',
            target_id=contact.id,
            details={'name': contact.name},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def perform_destroy(self, instance):
        log_admin_action(
            admin=self.request.user,
            action='emergency_contact_deleted',
            target_resource='emergency_contact',
            target_id=instance.id,
            details={'name': instance.name},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        instance.delete()
