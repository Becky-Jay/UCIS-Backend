from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdmin
from utils.audit_log import log_admin_action
from .models import Deadline, AlmanacEvent
from .serializers import DeadlineSerializer, AlmanacEventSerializer


class DeadlineListCreateView(generics.ListCreateAPIView):
    serializer_class = DeadlineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Deadline.objects.select_related('created_by').filter(
            is_active=True, deadline_date__gte=timezone.now()
        )
        if user.role not in ('system_admin', 'college_admin'):
            qs = qs.filter(
                target_roles__contains=user.role,
                college=user.college,
            )
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        deadline = serializer.save(created_by=self.request.user)
        log_admin_action(
            admin=self.request.user,
            action='deadline_created',
            target_resource='deadline',
            target_id=deadline.id,
            details={'title': deadline.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Deadlines fetched', 'deadlines': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Deadline created', 'deadline': response.data}, status=status.HTTP_201_CREATED)


class DeadlineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeadlineSerializer
    queryset = Deadline.objects.select_related('created_by').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]


class AlmanacEventListCreateView(generics.ListCreateAPIView):
    serializer_class = AlmanacEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = AlmanacEvent.objects.select_related('created_by').filter(is_public=True)
        year = self.request.query_params.get('year')
        category = self.request.query_params.get('category')
        if year:
            qs = qs.filter(academic_year=year)
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        event = serializer.save(created_by=self.request.user)
        log_admin_action(
            admin=self.request.user,
            action='almanac_event_created',
            target_resource='almanac_event',
            target_id=event.id,
            details={'title': event.title, 'academic_year': event.academic_year},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Almanac events fetched', 'events': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Almanac event created', 'event': response.data}, status=status.HTTP_201_CREATED)


class AlmanacEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlmanacEventSerializer
    queryset = AlmanacEvent.objects.select_related('created_by').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]
