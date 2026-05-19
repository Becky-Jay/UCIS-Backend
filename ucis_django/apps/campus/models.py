from django.db import models


class CampusLocation(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic Building'),
        ('admin', 'Administration'),
        ('library', 'Library'),
        ('medical', 'Medical / Health'),
        ('security', 'Security'),
        ('sports', 'Sports & Recreation'),
        ('food', 'Food & Cafeteria'),
        ('religious', 'Religious'),
        ('transport', 'Transport'),
        ('hostel', 'Hostel / Residence'),
        ('lab', 'Laboratory'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    building_code = models.CharField(max_length=20, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)
    opening_hours = models.JSONField(default=dict, blank=True)
    college = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='campus_locations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'campus_locations'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'


class LocationSearchHistory(models.Model):
    location = models.ForeignKey(
        CampusLocation, on_delete=models.CASCADE, related_name='search_history'
    )
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='location_searches'
    )
    searched_at = models.DateTimeField(auto_now_add=True)
    search_query = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = 'location_search_history'
        ordering = ['-searched_at']

    def __str__(self):
        return f'{self.user.username} searched "{self.search_query}"'
