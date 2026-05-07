from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer


class MyNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Notifications fetched',
            'notifications': serializer.data,
            'unread_count': queryset.filter(seen=False).count(),
        })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_seen(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.seen = True
    notification.save(update_fields=['seen'])
    return Response({'message': 'Notification marked as seen'})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_all_seen(request):
    Notification.objects.filter(user=request.user, seen=False).update(seen=True)
    return Response({'message': 'All notifications marked as seen'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    return Response({'message': 'Notification deleted'}, status=status.HTTP_204_NO_CONTENT)
