from django.db import models


class EventMedia(models.Model):
    MEDIA_TYPE_CHOICES = [('image', 'Image'), ('video', 'Video')]
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='media')
    url = models.URLField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    class Meta:
        db_table = 'event_media'


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    organizer = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(null=True, blank=True)
    start_time = models.CharField(max_length=10, blank=True)
    max_attendees = models.IntegerField()
    attendees = models.ManyToManyField('users.User', related_name='attended_events', blank=True)
    registration_link = models.URLField(blank=True)
    college = models.JSONField(default=list, blank=True)
    department = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    target_roles = models.JSONField(default=list)
    location = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EventSubscription(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='event_subscriptions')
    subscribed_at = models.DateTimeField(auto_now_add=True)
    reminder_enabled = models.BooleanField(default=False)

    class Meta:
        db_table = 'event_subscriptions'
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.user.username} → {self.event.title}'
