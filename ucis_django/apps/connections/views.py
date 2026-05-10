from django.utils import timezone
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Connection, Message
from .serializers import ConnectionSerializer, MessageSerializer


class ConnectionListCreateView(generics.ListCreateAPIView):
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        conn_status = self.request.query_params.get('status')
        qs = Connection.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'sender__profile', 'receiver', 'receiver__profile')
        if conn_status:
            qs = qs.filter(status=conn_status)
        return qs

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        if Connection.objects.filter(sender=self.request.user, receiver_id=receiver_id).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Connection request already sent.')
        serializer.save(sender=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Connections fetched', 'connections': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Connection request sent', 'connection': response.data}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def respond_to_connection(request, pk):
    connection = get_object_or_404(Connection, pk=pk, receiver=request.user)
    new_status = request.data.get('status')
    if new_status not in ('accepted', 'rejected', 'blocked'):
        return Response({'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    connection.status = new_status
    connection.save(update_fields=['status', 'updated_at'])
    return Response({'message': f'Connection {new_status}', 'connection': ConnectionSerializer(connection).data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_connection(request, pk):
    connection = get_object_or_404(
        Connection, pk=pk
    )
    if connection.sender != request.user and connection.receiver != request.user:
        return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    connection.delete()
    return Response({'message': 'Connection removed'}, status=status.HTTP_204_NO_CONTENT)


class ConversationView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.kwargs['user_id']
        return Message.objects.filter(
            Q(sender=self.request.user, recipient_id=other_user_id) |
            Q(sender_id=other_user_id, recipient=self.request.user)
        ).select_related('sender', 'recipient').order_by('created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.filter(recipient=request.user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Conversation fetched', 'messages': serializer.data})

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, recipient_id=self.kwargs['user_id'])

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Message sent', 'message': response.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inbox(request):
    from django.db.models import Max
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).values('sender', 'recipient').annotate(last_message=Max('created_at')).order_by('-last_message')
    unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
    return Response({'message': 'Inbox fetched', 'unread_count': unread_count, 'threads': list(messages)})
