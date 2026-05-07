import logging
from django.conf import settings

logger = logging.getLogger(__name__)

_firebase_initialized = False


def _get_firebase_app():
    global _firebase_initialized
    if _firebase_initialized:
        return
    if not settings.FIREBASE_CREDENTIALS_PATH:
        return
    try:
        import firebase_admin
        from firebase_admin import credentials
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
    except Exception as e:
        logger.error(f'Firebase init failed: {e}')


def send_push_notification(fcm_tokens, title, body, data=None):
    """Send FCM push notification to a list of tokens."""
    if not fcm_tokens:
        return
    _get_firebase_app()
    try:
        from firebase_admin import messaging
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            tokens=fcm_tokens,
        )
        response = messaging.send_each_for_multicast(message)
        logger.info(f'FCM: {response.success_count} sent, {response.failure_count} failed')
    except Exception as e:
        logger.error(f'FCM send failed: {e}')


def notify_announcement(announcement):
    """Notify users about a new announcement."""
    from apps.users.models import User
    from apps.notifications.models import Notification

    users = User.objects.filter(
        role__in=announcement.target_roles,
        is_active=True,
    )
    if announcement.college:
        users = users.filter(college__in=announcement.college)

    notifications = [
        Notification(
            user=u,
            title=announcement.title,
            body=announcement.content[:200],
            source_type='announcement',
            source_id=str(announcement.id),
            delivered_via=['in-app'],
        )
        for u in users
    ]
    Notification.objects.bulk_create(notifications, ignore_conflicts=True)

    all_tokens = []
    for u in users:
        all_tokens.extend(u.fcm_tokens or [])
    send_push_notification(all_tokens, announcement.title, announcement.content[:200])


def notify_admin_action(college, message, action_type, log_id=None):
    """Notify admins of a college about an administrative action."""
    from apps.users.models import User
    from apps.notifications.models import Notification

    admins = User.objects.filter(
        role__in=['system_admin', 'college_admin'],
        is_active=True,
    )
    if college:
        admins = admins.filter(college__in=college if isinstance(college, list) else [college])

    notifications = [
        Notification(
            user=admin,
            title=action_type,
            body=message,
            source_type='admin_action',
            source_id=str(log_id) if log_id else '0',
            delivered_via=['in-app'],
        )
        for admin in admins
    ]
    Notification.objects.bulk_create(notifications, ignore_conflicts=True)
