from django.db import models


class NewsMedia(models.Model):
    MEDIA_TYPE_CHOICES = [('image', 'Image'), ('video', 'Video')]
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='media')
    url = models.URLField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    class Meta:
        db_table = 'news_media'


class News(models.Model):
    CATEGORY_CHOICES = [
        ('sports', 'Sports'),
        ('technology', 'Technology'),
        ('health', 'Health'),
        ('academics', 'Academics'),
        ('alumni', 'Alumni'),
        ('students_life', "Students' Life"),
        ('career_fair', 'Career Fair'),
    ]

    title = models.CharField(max_length=300)
    content = models.TextField()
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='news')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list, blank=True)
    target_roles = models.JSONField(default=list)
    college = models.JSONField(default=list)
    is_published = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'news'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
