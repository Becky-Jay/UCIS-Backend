from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('college_admin', 'College Admin'),
        ('system_admin', 'System Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    college = models.CharField(max_length=100, blank=True)
    fcm_tokens = models.JSONField(default=list, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['email', 'role']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.username} ({self.role})'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)
    mentorship_availability = models.BooleanField(default=False)
    interests = models.JSONField(default=list, blank=True)
    notification_preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    degree_course = models.CharField(max_length=200, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    college = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'user_education'


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experience')
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_work_experience'


class Expertise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expertise')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    class Meta:
        db_table = 'user_expertise'


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'user_achievements'


class Relationship(models.Model):
    TYPE_CHOICES = [
        ('connected', 'Connected'),
        ('following', 'Following'),
    ]
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationships')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    relationship_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='following')

    class Meta:
        db_table = 'user_relationships'
        unique_together = ('from_user', 'to_user')


class StudentEngagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_engagement')
    posts_created = models.IntegerField(default=0)
    alumni_connections = models.IntegerField(default=0)
    events_registered = models.IntegerField(default=0)
    events_attended = models.IntegerField(default=0)
    mentorship_requests = models.IntegerField(default=0)
    active_mentorships = models.IntegerField(default=0)
    last_engagement_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'student_engagement'


class AlumniEngagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_engagement')
    posts_created = models.IntegerField(default=0)
    events_registered = models.IntegerField(default=0)
    events_attended = models.IntegerField(default=0)
    mentees_count = models.IntegerField(default=0)
    career_advice_sessions = models.IntegerField(default=0)
    networking_events = models.IntegerField(default=0)
    last_engagement_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'alumni_engagement'


class SystemAdminEngagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='system_admin_engagement')
    events_created = models.IntegerField(default=0)
    announcements_created = models.IntegerField(default=0)
    users_managed = models.IntegerField(default=0)
    system_actions = models.IntegerField(default=0)
    last_engagement_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'system_admin_engagement'


class CollegeAdminEngagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='college_admin_engagement')
    events_created = models.IntegerField(default=0)
    announcements_created = models.IntegerField(default=0)
    college_users_managed = models.IntegerField(default=0)
    college_actions = models.IntegerField(default=0)
    last_engagement_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'college_admin_engagement'
