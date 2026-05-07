from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.users.permissions import IsAdmin
from utils.audit_log import log_admin_action
from .models import Event
from .serializers import EventSerializer


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Event.objects.select_related('created_by').prefetch_related('media', 'attendees')

        if user.role in ('system_admin', 'college_admin'):
            return qs

        return qs.filter(
            target_roles__contains=user.role,
            status='active',
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        event = serializer.save(created_by=self.request.user)
        log_admin_action(
            admin=self.request.user,
            action='event_created',
            target_resource='event',
            target_id=event.id,
            details={'title': event.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Events fetched successfully', 'events': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Event created successfully', 'event': response.data}, status=status.HTTP_201_CREATED)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.select_related('created_by').prefetch_related('media', 'attendees').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def perform_update(self, serializer):
        event = serializer.save()
        log_admin_action(
            admin=self.request.user,
            action='event_updated',
            target_resource='event',
            target_id=event.id,
            details={'title': event.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def perform_destroy(self, instance):
        log_admin_action(
            admin=self.request.user,
            action='event_deleted',
            target_resource='event',
            target_id=instance.id,
            details={'title': instance.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.attendees.count() >= event.max_attendees:
        return Response({'message': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)
    event.attendees.add(request.user)
    return Response({'message': 'Registered for event successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unregister_from_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.attendees.remove(request.user)
    return Response({'message': 'Unregistered from event successfully'})
