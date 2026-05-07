from django.db import models


class MentorshipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    student = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='mentorship_requests_sent'
    )
    alumni = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='mentorship_requests_received'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentorship_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.username} → {self.alumni.username} ({self.status})'
