import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_email(to, subject, text, html=None):
    try:
        send_mail(
            subject=subject,
            message=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to] if isinstance(to, str) else to,
            html_message=html,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f'Failed to send email to {to}: {e}')
        raise
