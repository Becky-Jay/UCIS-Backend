from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.users.permissions import IsAdmin, IsAlumni
from utils.audit_log import log_admin_action
from .models import AlumniProfile
from .serializers import AlumniProfileSerializer, AlumniProfileCreateUpdateSerializer


class AlumniProfileListView(generics.ListAPIView):
    serializer_class = AlumniProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = AlumniProfile.objects.select_related('user', 'user__profile').all()
        industry = self.request.query_params.get('industry')
        mentorship = self.request.query_params.get('mentorship')
        if industry:
            qs = qs.filter(industry__icontains=industry)
        if mentorship:
            qs = qs.filter(joined_mentorship=True)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'Alumni fetched successfully', 'alumni': serializer.data})


class AlumniProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return AlumniProfileCreateUpdateSerializer
        return AlumniProfileSerializer

    def get_queryset(self):
        return AlumniProfile.objects.select_related('user', 'user__profile').all()

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user and request.user.role not in ('system_admin', 'college_admin'):
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAlumni])
def create_or_update_my_profile(request):
    profile, created = AlumniProfile.objects.get_or_create(
        user=request.user,
        defaults={'graduation_year': request.data.get('graduation_year', 0)},
    )
    serializer = AlumniProfileCreateUpdateSerializer(profile, data=request.data, partial=not created)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    msg = 'Alumni profile created' if created else 'Alumni profile updated'
    return Response(
        {'message': msg, 'profile': AlumniProfileSerializer(profile).data},
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdmin])
def verify_alumni(request, pk):
    profile = get_object_or_404(AlumniProfile, pk=pk)
    profile.is_verified = True
    profile.save(update_fields=['is_verified'])
    log_admin_action(
        admin=request.user,
        action='alumni_verified',
        target_resource='alumni_profile',
        target_id=profile.id,
        details={'username': profile.user.username},
        ip_address=request.META.get('REMOTE_ADDR'),
    )
    return Response({'message': 'Alumni verified successfully'})
