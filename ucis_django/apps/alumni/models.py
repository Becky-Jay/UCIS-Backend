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
