from django.contrib import admin
from .models import Event, EventMedia


class EventMediaInline(admin.TabularInline):
    model = EventMedia
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventMediaInline]
    list_display = ('title', 'category', 'organizer', 'date', 'status', 'max_attendees', 'created_by')
    list_filter = ('category', 'status')
    search_fields = ('title', 'organizer', 'location')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('attendees',)
