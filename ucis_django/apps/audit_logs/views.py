from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from apps.users.permissions import IsAdmin
from .models import AuditLog
from .serializers import AuditLogSerializer


def _base_queryset(user):
    qs = AuditLog.objects.select_related('performed_by').all()
    if user.role == 'college_admin':
        qs = qs.filter(performed_by__college=user.college)
    return qs


class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['action', 'role', 'target_resource', 'target_id', 'performed_by', 'ip_address']
    ordering_fields = ['timestamp', 'action', 'role']
    ordering = ['-timestamp']

    def get_queryset(self):
        qs = _base_queryset(self.request.user)
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(timestamp__date__gte=date_from)
        if date_to:
            qs = qs.filter(timestamp__date__lte=date_to)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Audit logs fetched', 'logs': serializer.data})


class AuditLogDetailView(generics.RetrieveAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self):
        qs = _base_queryset(self.request.user)
        try:
            return qs.get(pk=self.kwargs['pk'])
        except AuditLog.DoesNotExist:
            raise NotFound('Audit log not found.')


class AuditLogByUserView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [OrderingFilter]
    ordering_fields = ['timestamp', 'action']
    ordering = ['-timestamp']

    def get_queryset(self):
        return _base_queryset(self.request.user).filter(performed_by__id=self.kwargs['user_id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'User audit logs fetched', 'logs': serializer.data})


class AuditLogByResourceView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [OrderingFilter]
    ordering_fields = ['timestamp', 'action']
    ordering = ['-timestamp']

    def get_queryset(self):
        return _base_queryset(self.request.user).filter(
            target_resource=self.kwargs['resource'],
            target_id=self.kwargs['target_id'],
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Resource audit logs fetched', 'logs': serializer.data})


class AuditLogStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        qs = _base_queryset(request.user)
        by_action = list(qs.values('action').annotate(count=Count('id')).order_by('-count'))
        by_role = list(qs.values('role').annotate(count=Count('id')).order_by('-count'))
        by_resource = list(qs.values('target_resource').annotate(count=Count('id')).order_by('-count'))
        top_users = list(
            qs.values('performed_by__id', 'performed_by__username')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        return Response({
            'message': 'Audit log stats fetched',
            'total': qs.count(),
            'by_action': by_action,
            'by_role': by_role,
            'by_resource': by_resource,
            'top_users': top_users,
        })
