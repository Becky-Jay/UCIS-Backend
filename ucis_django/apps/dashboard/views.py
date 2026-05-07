from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count

from apps.users.permissions import IsAdmin, IsSystemAdmin, IsCollegeAdmin
from apps.users.models import User, StudentEngagement, AlumniEngagement
from apps.announcements.models import Announcement
from apps.events.models import Event
from apps.mentorship.models import MentorshipRequest
from apps.audit_logs.models import AuditLog


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def dashboard_stats(request):
    user = request.user
    now = timezone.now()

    if user.role == 'system_admin':
        stats = _system_admin_stats(now)
    else:
        stats = _college_admin_stats(user, now)

    return Response({'message': 'Dashboard stats fetched', 'stats': stats})


def _system_admin_stats(now):
    total_users = User.objects.count()
    by_role = dict(User.objects.values_list('role').annotate(count=Count('id')).values_list('role', 'count'))
    active_users = User.objects.filter(is_active=True).count()
    total_events = Event.objects.count()
    active_events = Event.objects.filter(status='active', date__gte=now.date()).count()
    active_announcements = Announcement.objects.filter(expires_at__gt=now, is_published=True).count()
    pending_mentorships = MentorshipRequest.objects.filter(status='pending').count()
    recent_logs = list(
        AuditLog.objects.order_by('-timestamp')[:10].values(
            'id', 'action', 'role', 'target_resource', 'timestamp', 'ip_address'
        )
    )

    return {
        'total_users': total_users,
        'active_users': active_users,
        'users_by_role': by_role,
        'total_events': total_events,
        'active_events': active_events,
        'active_announcements': active_announcements,
        'pending_mentorships': pending_mentorships,
        'recent_audit_logs': recent_logs,
    }


def _college_admin_stats(user, now):
    college = user.college
    college_users = User.objects.filter(college=college)
    total_college_users = college_users.count()
    active_college_users = college_users.filter(is_active=True).count()

    college_events = Event.objects.filter(college__contains=college)
    active_events = college_events.filter(status='active', date__gte=now.date()).count()

    college_announcements = Announcement.objects.filter(
        college__contains=college, expires_at__gt=now, is_published=True
    ).count()

    recent_logs = list(
        AuditLog.objects.filter(performed_by__college=college)
        .order_by('-timestamp')[:10]
        .values('id', 'action', 'role', 'target_resource', 'timestamp')
    )

    return {
        'college': college,
        'total_users': total_college_users,
        'active_users': active_college_users,
        'active_events': active_events,
        'active_announcements': college_announcements,
        'recent_audit_logs': recent_logs,
    }


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    if request.user.role != 'student':
        from rest_framework import status
        return Response({'message': 'Forbidden'}, status=403)

    user = request.user
    now = timezone.now()
    eng = getattr(user, 'student_engagement', None)

    upcoming_events = Event.objects.filter(
        target_roles__contains='student',
        status='active',
        date__gte=now.date(),
    ).order_by('date')[:5].values('id', 'title', 'date', 'location', 'category')

    recent_announcements = Announcement.objects.filter(
        target_roles__contains='student',
        college__contains=user.college,
        expires_at__gt=now,
    ).order_by('-created_at')[:5].values('id', 'title', 'category', 'created_at')

    pending_mentorships = MentorshipRequest.objects.filter(
        student=user, status='pending'
    ).count()

    return Response({
        'message': 'Student dashboard fetched',
        'dashboard': {
            'engagement': {
                'posts_created': eng.posts_created if eng else 0,
                'events_registered': eng.events_registered if eng else 0,
                'mentorship_requests': eng.mentorship_requests if eng else 0,
                'active_mentorships': eng.active_mentorships if eng else 0,
            },
            'upcoming_events': list(upcoming_events),
            'recent_announcements': list(recent_announcements),
            'pending_mentorships': pending_mentorships,
        },
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alumni_dashboard(request):
    if request.user.role != 'alumni':
        return Response({'message': 'Forbidden'}, status=403)

    user = request.user
    now = timezone.now()
    eng = getattr(user, 'alumni_engagement', None)

    mentorship_requests = MentorshipRequest.objects.filter(alumni=user, status='pending').count()

    upcoming_events = Event.objects.filter(
        target_roles__contains='alumni',
        status='active',
        date__gte=now.date(),
    ).order_by('date')[:5].values('id', 'title', 'date', 'location', 'category')

    return Response({
        'message': 'Alumni dashboard fetched',
        'dashboard': {
            'engagement': {
                'posts_created': eng.posts_created if eng else 0,
                'events_attended': eng.events_attended if eng else 0,
                'mentees_count': eng.mentees_count if eng else 0,
            },
            'pending_mentorship_requests': mentorship_requests,
            'upcoming_events': list(upcoming_events),
        },
    })
