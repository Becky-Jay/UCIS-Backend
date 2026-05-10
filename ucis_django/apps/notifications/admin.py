from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'source_type', 'seen', 'sent_at')
    list_filter = ('source_type', 'seen')
    search_fields = ('user__username', 'title', 'body')
    readonly_fields = ('sent_at',)
