from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_by', 'is_published', 'expires_at', 'created_at')
    list_filter = ('category', 'is_published', 'visibility')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
