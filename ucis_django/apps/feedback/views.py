from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.users.permissions import IsAdmin
from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackAdminSerializer


class FeedbackListCreateView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('system_admin', 'college_admin'):
            qs = Feedback.objects.select_related('user', 'reviewed_by').all()
            status_filter = self.request.query_params.get('status')
            category = self.request.query_params.get('category')
            if status_filter:
                qs = qs.filter(status=status_filter)
            if category:
                qs = qs.filter(category=category)
            return qs
        return Feedback.objects.filter(user=user).select_related('user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Feedback fetched', 'feedback': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Feedback submitted', 'feedback': response.data}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdmin])
def respond_to_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    serializer = FeedbackAdminSerializer(feedback, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save(reviewed_by=request.user)
    return Response({'message': 'Feedback updated', 'feedback': FeedbackSerializer(feedback).data})
