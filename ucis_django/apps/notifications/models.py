from django.db import models


class Notification(models.Model):
    SOURCE_TYPES = [
        ('announcement', 'Announcement'),
        ('news', 'News'),
        ('event', 'Event'),
        ('mentorship', 'Mentorship'),
        ('admin_action', 'Admin Action'),
        ('general', 'General'),
    ]
    DELIVERY_CHANNELS = [
        ('push', 'Push'),
        ('email', 'Email'),
        ('in-app', 'In-App'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPES)
    source_id = models.CharField(max_length=50)
    seen = models.BooleanField(default=False)
    delivered_via = models.JSONField(default=list)
    sent_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.user.username}: {self.title}'
