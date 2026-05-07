from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdmin
from utils.audit_log import log_admin_action
from .models import News
from .serializers import NewsSerializer


class NewsListCreateView(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = News.objects.filter(is_archived=False).select_related('created_by').prefetch_related('media')

        if user.role in ('system_admin', 'college_admin'):
            return qs

        return qs.filter(
            target_roles__contains=user.role,
            college__contains=user.college,
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        news = serializer.save(created_by=self.request.user)
        log_admin_action(
            admin=self.request.user,
            action='news_created',
            target_resource='news',
            target_id=news.id,
            details={'title': news.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': 'News fetched successfully', 'news': serializer.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'News created successfully', 'news': response.data}, status=status.HTTP_201_CREATED)


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.select_related('created_by').prefetch_related('media').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def perform_update(self, serializer):
        news = serializer.save()
        log_admin_action(
            admin=self.request.user,
            action='news_updated',
            target_resource='news',
            target_id=news.id,
            details={'title': news.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )

    def perform_destroy(self, instance):
        log_admin_action(
            admin=self.request.user,
            action='news_deleted',
            target_resource='news',
            target_id=instance.id,
            details={'title': instance.title},
            ip_address=self.request.META.get('REMOTE_ADDR'),
        )
        instance.delete()
