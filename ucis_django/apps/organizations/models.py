from django.db import models


class StudentsOrganization(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ]

    org_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = 'students_organizations'
        ordering = ['org_name']

    def __str__(self):
        return self.org_name


class OrganizationMember(models.Model):
    org = models.ForeignKey(
        StudentsOrganization, on_delete=models.CASCADE, related_name='members'
    )
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='organization_memberships'
    )
    role = models.CharField(max_length=100, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organization_members'
        unique_together = ('org', 'user')

    def __str__(self):
        return f'{self.user.username} @ {self.org.org_name} ({self.role})'
