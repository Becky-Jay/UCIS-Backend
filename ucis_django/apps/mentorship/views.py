from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.users.permissions import IsStudent, IsAlumni, IsAdmin
from .models import MentorshipRequest
from .serializers import MentorshipRequestSerializer


class MentorshipRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = MentorshipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return MentorshipRequest.objects.filter(student=user).select_related('student', 'alumni')
        if user.role == 'alumni':
            return MentorshipRequest.objects.filter(alumni=user).select_related('student', 'alumni')
        return MentorshipRequest.objects.select_related('student', 'alumni').all()

    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only students can send mentorship requests.')
        request = serializer.save(student=self.request.user)
        eng = getattr(self.request.user, 'student_engagement', None)
        if eng:
            eng.mentorship_requests += 1
            eng.save(update_fields=['mentorship_requests'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Mentorship requests fetched', 'requests': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Mentorship request sent', 'request': response.data}, status=status.HTTP_201_CREATED)


class MentorshipRequestDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MentorshipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MentorshipRequest.objects.select_related('student', 'alumni').all()

    def update(self, request, *args, **kwargs):
        mentorship = self.get_object()
        new_status = request.data.get('status')

        if request.user.role == 'alumni' and mentorship.alumni != request.user:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        if new_status == 'approved' and request.user.role == 'alumni':
            eng = getattr(request.user, 'alumni_engagement', None)
            if eng:
                eng.mentees_count += 1
                eng.save(update_fields=['mentees_count'])
            student_eng = getattr(mentorship.student, 'student_engagement', None)
            if student_eng:
                student_eng.active_mentorships += 1
                student_eng.save(update_fields=['active_mentorships'])

        return super().update(request, *args, **kwargs)
