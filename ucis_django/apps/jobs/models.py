from django.db import models


class JobOpportunity(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
        ('volunteer', 'Volunteer'),
    ]

    title = models.CharField(max_length=300)
    company = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    location = models.CharField(max_length=200, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    application_link = models.URLField(blank=True)
    target_roles = models.JSONField(default=list)
    college = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    posted_by = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='job_postings'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_opportunities'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} at {self.company}'


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_applications'
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f'{self.applicant.username} → {self.job.title}'
