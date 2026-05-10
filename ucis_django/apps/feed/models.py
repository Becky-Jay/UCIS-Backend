from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    college = models.CharField(max_length=100, blank=True)
    target_roles = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    posted_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('celebrate', 'Celebrate'),
        ('support', 'Support'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_reactions'
        unique_together = ('post', 'user')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_comments'
        ordering = ['created_at']


class Story(models.Model):
    MEDIA_TYPE_CHOICES = [('image', 'Image'), ('video', 'Video'), ('text', 'Text')]

    posted_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='stories')
    content = models.TextField(blank=True)
    media_url = models.URLField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='text')
    background_color = models.CharField(max_length=20, blank=True, default='#1a1a2e')
    viewers = models.ManyToManyField('users.User', related_name='viewed_stories', blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stories'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.posted_by.username} story ({self.created_at.date()})'

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
