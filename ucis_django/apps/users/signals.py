from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    User, UserProfile, StudentEngagement,
    AlumniEngagement, SystemAdminEngagement, CollegeAdminEngagement,
)


@receiver(post_save, sender=User)
def create_user_profile_and_engagement(sender, instance, created, **kwargs):
    if not created:
        return

    UserProfile.objects.get_or_create(
        user=instance,
        defaults={
            'first_name': instance.first_name or '',
            'last_name': instance.last_name or '',
            'notification_preferences': {
                'events': True,
                'news': True,
                'announcements': True,
                'mentorship': True,
                'opportunities': True,
                'social': True,
            },
        },
    )

    if instance.role == 'student':
        StudentEngagement.objects.get_or_create(user=instance)
    elif instance.role == 'alumni':
        AlumniEngagement.objects.get_or_create(user=instance)
    elif instance.role == 'system_admin':
        SystemAdminEngagement.objects.get_or_create(user=instance)
    elif instance.role == 'college_admin':
        CollegeAdminEngagement.objects.get_or_create(user=instance)
