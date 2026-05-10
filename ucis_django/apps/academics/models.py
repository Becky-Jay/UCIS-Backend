from django.db import models


class Deadline(models.Model):
    CATEGORY_CHOICES = [
        ('assignment', 'Assignment'),
        ('exam', 'Exam'),
        ('registration', 'Registration'),
        ('project', 'Project / FYP'),
        ('fee', 'Fee Payment'),
        ('application', 'Application'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    deadline_date = models.DateTimeField()
    course = models.CharField(max_length=200, blank=True)
    college = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    target_roles = models.JSONField(default=list)
    created_by = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='deadlines'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'deadlines'
        ordering = ['deadline_date']

    def __str__(self):
        return f'{self.title} — {self.deadline_date.date()}'


class AlmanacEvent(models.Model):
    CATEGORY_CHOICES = [
        ('semester_start', 'Semester Start'),
        ('semester_end', 'Semester End'),
        ('exam_period', 'Exam Period'),
        ('holiday', 'Public Holiday'),
        ('registration', 'Registration Period'),
        ('graduation', 'Graduation'),
        ('orientation', 'Orientation'),
        ('sports', 'Sports Week'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    academic_year = models.CharField(max_length=20, blank=True)
    college = models.JSONField(default=list, blank=True)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='almanac_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'almanac_events'
        ordering = ['start_date']

    def __str__(self):
        return f'{self.title} ({self.academic_year})'
