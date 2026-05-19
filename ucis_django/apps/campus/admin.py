from django.contrib import admin
from .models import CampusLocation, LocationSearchHistory


@admin.register(CampusLocation)
class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'college', 'building_code', 'is_active', 'created_at')
    list_filter = ('category', 'college', 'is_active')
    search_fields = ('name', 'description', 'building_code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LocationSearchHistory)
class LocationSearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'search_query', 'searched_at')
    list_filter = ('location',)
    search_fields = ('user__username', 'search_query', 'location__name')
    readonly_fields = ('searched_at',)
