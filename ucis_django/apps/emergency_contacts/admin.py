from django.contrib import admin
from .models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'phone', 'location', 'priority')
    list_filter = ('category',)
    search_fields = ('name', 'phone', 'description')
    ordering = ('priority',)
