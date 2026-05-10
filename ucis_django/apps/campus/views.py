from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdmin
from utils.audit_log import log_admin_action
from .models import CampusLocation
from .serializers import CampusLocationSerializer


class CampusLocationListCreateView(generics.ListCreateAPIView):
    serializer_class = CampusLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = CampusLocation.objects.select_related('created_by').filter(is_active=True)
        category = self.request.query_params.get('category')
        college = self.request.query_params.get('college')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category=category)
        if college:
            qs = qs.filter(college=college)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        location = serializer.save(created_by=self.request.user)
        log_admin_action(
            admin=self.request.user,
            action='campus_location_created',
            target_resource='campus_location',
            target_id=location.id,
            details={'name': location.name, 'category': location.category},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Campus locations fetched', 'locations': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Campus location created', 'location': response.data}, status=status.HTTP_201_CREATED)


class CampusLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CampusLocationSerializer
    queryset = CampusLocation.objects.select_related('created_by').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def perform_update(self, serializer):
        location = serializer.save()
        log_admin_action(
            admin=self.request.user,
            action='campus_location_updated',
            target_resource='campus_location',
            target_id=location.id,
            details={'name': location.name},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def perform_destroy(self, instance):
        log_admin_action(
            admin=self.request.user,
            action='campus_location_deleted',
            target_resource='campus_location',
            target_id=instance.id,
            details={'name': instance.name},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        instance.delete()
