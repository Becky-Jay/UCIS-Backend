from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.users.permissions import IsAdmin
from utils.audit_log import log_admin_action
from .models import JobOpportunity, JobApplication
from .serializers import JobOpportunitySerializer, JobApplicationSerializer


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobOpportunitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = JobOpportunity.objects.select_related('posted_by').filter(is_active=True)
        job_type = self.request.query_params.get('type')
        industry = self.request.query_params.get('industry')
        search = self.request.query_params.get('search')
        if job_type:
            qs = qs.filter(job_type=job_type)
        if industry:
            qs = qs.filter(industry__icontains=industry)
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(company__icontains=search)
        if user.role not in ('system_admin', 'college_admin'):
            qs = qs.filter(target_roles__contains=user.role)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'request': self.request}

    def perform_create(self, serializer):
        job = serializer.save(posted_by=self.request.user)
        log_admin_action(
            admin=self.request.user,
            action='job_created',
            target_resource='job_opportunity',
            target_id=job.id,
            details={'title': job.title, 'company': job.company},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Jobs fetched', 'jobs': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Job posted', 'job': response.data}, status=status.HTTP_201_CREATED)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobOpportunitySerializer
    queryset = JobOpportunity.objects.select_related('posted_by').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'request': self.request}

    def perform_destroy(self, instance):
        log_admin_action(
            admin=self.request.user,
            action='job_deleted',
            target_resource='job_opportunity',
            target_id=instance.id,
            details={'title': instance.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_job(request, pk):
    job = get_object_or_404(JobOpportunity, pk=pk, is_active=True)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        return Response({'message': 'You have already applied for this job'}, status=status.HTTP_400_BAD_REQUEST)
    application = JobApplication.objects.create(
        job=job,
        applicant=request.user,
        cover_letter=request.data.get('cover_letter', ''),
    )
    return Response({'message': 'Application submitted', 'application': JobApplicationSerializer(application).data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def job_applications(request, pk):
    job = get_object_or_404(JobOpportunity, pk=pk)
    applications = JobApplication.objects.filter(job=job).select_related('applicant')
    return Response({'message': 'Applications fetched', 'applications': JobApplicationSerializer(applications, many=True).data})
