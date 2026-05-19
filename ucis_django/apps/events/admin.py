from django.contrib import admin
from .models import Event, EventMedia, EventSubscription


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


@admin.register(EventSubscription)
class EventSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'reminder_enabled', 'subscribed_at')
    list_filter = ('reminder_enabled',)
    search_fields = ('user__username', 'event__title')
    readonly_fields = ('subscribed_at',)
