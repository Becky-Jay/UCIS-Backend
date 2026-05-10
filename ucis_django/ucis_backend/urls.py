from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def root(request):
    return Response({'message': 'UCIS Backend is running!', 'version': '2.0.0', 'framework': 'Django'})


urlpatterns = [
    path('', root, name='root'),
    path('admin/', admin.site.urls),

    path('api/authentication/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/announcements/', include('apps.announcements.urls')),
    path('api/news/', include('apps.news.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/feed/', include('apps.feed.urls')),
    path('api/mentorshipRequest/', include('apps.mentorship.urls')),
    path('api/alumni/', include('apps.alumni.urls')),
    path('api/emergencyContacts/', include('apps.emergency_contacts.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/auditLogs/', include('apps.audit_logs.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),

    path('api/campus/', include('apps.campus.urls')),
    path('api/jobs/', include('apps.jobs.urls')),
    path('api/academics/', include('apps.academics.urls')),
    path('api/connections/', include('apps.connections.urls')),
    path('api/feedback/', include('apps.feedback.urls')),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
