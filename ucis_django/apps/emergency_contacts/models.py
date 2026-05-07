from django.db import models


class EmergencyContact(models.Model):
    CATEGORY_CHOICES = [
        ('Medical', 'Medical'),
        ('Security', 'Security'),
        ('Fire', 'Fire'),
        ('Counseling', 'Counseling'),
    ]

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    priority = models.IntegerField(default=1)
    visible_to = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'emergency_contacts'
        ordering = ['priority']

    def __str__(self):
        return f'{self.name} ({self.category})'
