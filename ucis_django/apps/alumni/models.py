from django.db import models


class AlumniProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='alumni_profile')
    graduation_year = models.IntegerField()
    industry = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list, blank=True)
    achievements = models.JSONField(default=list, blank=True)
    company = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=100, blank=True)
    linked_in = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    joined_mentorship = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'alumni_profiles'

    def __str__(self):
        return f'{self.user.username} - Alumni {self.graduation_year}'


class AlumniConnection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    alumni_1 = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE, related_name='connections_initiated'
    )
    alumni_2 = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE, related_name='connections_received'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    connected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alumni_connections'
        unique_together = ('alumni_1', 'alumni_2')

    def __str__(self):
        return f'{self.alumni_1.user.username} ↔ {self.alumni_2.user.username} ({self.status})'
