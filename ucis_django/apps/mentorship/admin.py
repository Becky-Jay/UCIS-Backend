from django.contrib import admin
from .models import MentorshipRequest


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'alumni', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__username', 'alumni__username')
    readonly_fields = ('created_at', 'updated_at')
