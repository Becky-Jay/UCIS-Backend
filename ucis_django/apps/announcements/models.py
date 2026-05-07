from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('emergency', 'Emergency'),
        ('academic', 'Academic'),
        ('general', 'General'),
        ('opportunity', 'Opportunity'),
        ('event', 'Event'),
    ]
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=300)
    content = models.TextField()
    created_by = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='announcements'
    )
    target_roles = models.JSONField(default=list)
    college = models.JSONField(default=list)
    location_coordinates = models.JSONField(null=True, blank=True)
    location_radius = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_scheduled = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']

    def clean(self):
        if self.expires_at and self.expires_at <= timezone.now():
            raise ValidationError({'expires_at': 'Expiration date must be in the future.'})

    def __str__(self):
        return self.title
