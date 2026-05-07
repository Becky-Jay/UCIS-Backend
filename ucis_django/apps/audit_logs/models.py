from django.db import models


class AuditLog(models.Model):
    ROLE_CHOICES = [
        ('college_admin', 'College Admin'),
        ('system_admin', 'System Admin'),
        ('student', 'Student'),
        ('alumni', 'Alumni'),
    ]

    action = models.CharField(max_length=100)
    performed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    target_resource = models.CharField(max_length=100)
    target_id = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['performed_by', '-timestamp']),
            models.Index(fields=['action']),
            models.Index(fields=['target_resource', 'target_id']),
        ]

    def __str__(self):
        return f'{self.action} by {self.performed_by} at {self.timestamp}'
