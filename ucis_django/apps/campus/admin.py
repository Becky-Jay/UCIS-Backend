from django.contrib import admin
from .models import CampusLocation


@admin.register(CampusLocation)
class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'college', 'building_code', 'is_active', 'created_at')
    list_filter = ('category', 'college', 'is_active')
    search_fields = ('name', 'description', 'building_code')
    readonly_fields = ('created_at', 'updated_at')
