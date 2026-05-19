from django.contrib import admin
from .models import AlumniProfile, AlumniConnection


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'graduation_year', 'company', 'position', 'industry', 'is_verified', 'joined_mentorship')
    list_filter = ('is_verified', 'joined_mentorship', 'industry')
    search_fields = ('user__username', 'company', 'position')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AlumniConnection)
class AlumniConnectionAdmin(admin.ModelAdmin):
    list_display = ('alumni_1', 'alumni_2', 'status', 'connected_at')
    list_filter = ('status',)
    search_fields = ('alumni_1__user__username', 'alumni_2__user__username')
    readonly_fields = ('connected_at',)
