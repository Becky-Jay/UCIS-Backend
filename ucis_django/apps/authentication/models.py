from django.db import models


class FailedAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=150, blank=True)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    blocked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'failed_attempts'
        indexes = [models.Index(fields=['ip_address'])]

    def __str__(self):
        return f'{self.ip_address} — {self.attempts} attempts'

    def is_blocked(self):
        from django.utils import timezone
        return self.blocked_until and timezone.now() < self.blocked_until
