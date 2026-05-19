from django.db import models


class DashboardPreferences(models.Model):
    LAYOUT_CHOICES = [
        ('grid', 'Grid'),
        ('list', 'List'),
    ]

    user = models.OneToOneField(
        'users.User', on_delete=models.CASCADE, related_name='dashboard_preferences'
    )
    show_announcements = models.BooleanField(default=True)
    show_events = models.BooleanField(default=True)
    show_quick_links = models.BooleanField(default=True)
    layout_type = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='grid')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboard_preferences'

    def __str__(self):
        return f'{self.user.username} preferences'
