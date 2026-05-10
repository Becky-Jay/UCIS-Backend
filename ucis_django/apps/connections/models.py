from django.db import models


class Connection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ]

    sender = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='connections_sent'
    )
    receiver = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='connections_received'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'connections'
        unique_together = ('sender', 'receiver')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender.username} → {self.receiver.username} ({self.status})'


class Message(models.Model):
    sender = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='messages_sent'
    )
    recipient = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='messages_received'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username} → {self.recipient.username}'
